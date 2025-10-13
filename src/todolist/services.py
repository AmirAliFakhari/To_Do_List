# src/todolist/services.py

from datetime import datetime
from typing import Optional

from .models import Project, Task, Status
from .exceptions import (
    ProjectNameExistsError,
    ProjectLimitExceededError,
    ValidationError,
    ProjectNotFoundError,
    TaskLimitExceededError,
    TaskNotFoundError,
    InvalidDeadlineError, 
)

class ToDoService:
    """
    Contains the main business logic for the ToDoList application.
    It manages projects and tasks in memory.
    """
    def __init__(self, max_projects: int, max_tasks_per_project: int):
        """
        Initializes the ToDoService.

        :param max_projects: The maximum number of projects allowed.
        :param max_tasks_per_project: The maximum number of tasks allowed per project.
        """
        self._projects: list[Project] = []
        self._max_projects = max_projects
        self._max_tasks_per_project = max_tasks_per_project
        self._project_id_counter = 1
        self._task_id_counter = 1

    def _get_task_by_id(self, task_id: int) -> tuple[Project, Task]:
        """
        A private helper to find a task and its parent project by task ID.

        :param task_id: The ID of the task to find.
        :return: A tuple containing the parent project and the task.
        :raises TaskNotFoundError: If the task with the given ID is not found.
        """
        for project in self._projects:
            for task in project.tasks:
                if task.id == task_id:
                    return project, task
        raise TaskNotFoundError(f"Task with ID '{task_id}' not found.")

    # --- Project Methods ---
    def create_project(self, name: str, description: str) -> Project:
        """
        Creates a new project.

        :param name: The name of the project (max 30 characters).
        :param description: The description of the project (max 150 characters).
        :return: The newly created Project object.
        :raises ProjectNameExistsError: If a project with the same name already exists.
        :raises ProjectLimitExceededError: If the maximum number of projects has been reached.
        :raises ValidationError: If the name or description exceeds the character limit.
        """
        if any(p.name == name for p in self._projects):
            raise ProjectNameExistsError(f"Project with name '{name}' already exists.")
        if len(self._projects) >= self._max_projects:
            raise ProjectLimitExceededError(f"Cannot create more than {self._max_projects} projects.")
        if len(name) > 30:
            raise ValidationError("Project name cannot exceed 30 characters.")
        if len(description) > 150:
            raise ValidationError("Project description cannot exceed 150 characters.")
        
        new_project = Project(id=self._project_id_counter, name=name, description=description)
        self._projects.append(new_project)
        self._project_id_counter += 1
        return new_project

    def edit_project(
        self,
        project_id: int,
        new_name: Optional[str] = None,
        new_description: Optional[str] = None,
    ) -> Project:
        """
        Edits an existing project's name and/or description.

        :param project_id: The ID of the project to edit.
        :param new_name: The new name for the project.
        :param new_description: The new description for the project.
        :return: The updated Project object.
        :raises ProjectNotFoundError: If the project with the given ID is not found.
        :raises ValidationError: If the new name or description exceeds character limits.
        :raises ProjectNameExistsError: If another project with the new name already exists.
        """
        project_to_edit = next((p for p in self._projects if p.id == project_id), None)
        if not project_to_edit:
            raise ProjectNotFoundError(f"Project with ID '{project_id}' not found.")

        if new_name is not None:
            if len(new_name) > 30:
                raise ValidationError("Project name cannot exceed 30 characters.")
            if any(p.name == new_name and p.id != project_id for p in self._projects):
                raise ProjectNameExistsError(f"Another project with name '{new_name}' already exists.")
            project_to_edit.name = new_name

        if new_description is not None:
            if len(new_description) > 150:
                raise ValidationError("Project description cannot exceed 150 characters.")
            project_to_edit.description = new_description
            
        return project_to_edit

    def delete_project(self, project_id: int) -> None:
        """
        Finds a project by ID and deletes it, including all its tasks (Cascade Delete).

        :param project_id: The ID of the project to delete.
        :raises ProjectNotFoundError: If the project with the given ID is not found.
        """
        project_to_delete = next((p for p in self._projects if p.id == project_id), None)
        if not project_to_delete:
            raise ProjectNotFoundError(f"Project with ID '{project_id}' not found.")
        
        self._projects.remove(project_to_delete)

    def get_all_projects(self) -> list[Project]:
        """Returns a list of all projects."""
        return self._projects

    # --- Task Methods ---
    def add_task_to_project(
        self,
        project_id: int,
        task_title: str,
        task_description: str,
        deadline: Optional[datetime] = None,
    ) -> Task:
        """
        Adds a new task to a specific project.

        :param project_id: The ID of the project to add the task to.
        :param task_title: The title of the task (max 30 characters).
        :param task_description: The description of the task (max 150 characters).
        :param deadline: The deadline for the task.
        :return: The newly created Task object.
        :raises ProjectNotFoundError: If the project with the given ID is not found.
        :raises TaskLimitExceededError: If the project has reached its task limit.
        :raises ValidationError: If the title or description exceeds character limits.
        :raises InvalidDeadlineError: If the provided deadline is in the past.
        """
        project = next((p for p in self._projects if p.id == project_id), None)
        if project is None:
            raise ProjectNotFoundError(f"Project with ID '{project_id}' not found.")
        if len(project.tasks) >= self._max_tasks_per_project:
            raise TaskLimitExceededError(
                f"Cannot add more than {self._max_tasks_per_project} tasks to '{project.name}'."
            )
        if len(task_title) > 30:
            raise ValidationError("Task title cannot exceed 30 characters.")
        if len(task_description) > 150:
            raise ValidationError("Task description cannot exceed 150 characters.")
        if deadline and deadline < datetime.now():
            raise InvalidDeadlineError("Deadline cannot be in the past.")
        
        new_task = Task(
            id=self._task_id_counter,
            title=task_title,
            description=task_description,
            deadline=deadline,
        )
        project.tasks.append(new_task)
        self._task_id_counter += 1
        return new_task

    def edit_task(
        self,
        task_id: int,
        new_title: Optional[str] = None,
        new_description: Optional[str] = None,
        new_status: Optional[Status] = None,
        new_deadline: Optional[datetime] = None,
    ) -> Task:
        """
        Edits an existing task.

        :param task_id: The ID of the task to edit.
        :param new_title: The new title for the task.
        :param new_description: The new description for the task.
        :param new_status: The new status for the task.
        :param new_deadline: The new deadline for the task.
        :return: The updated Task object.
        :raises TaskNotFoundError: If the task with the given ID is not found.
        :raises ValidationError: If the new title or description exceeds character limits.
        :raises InvalidDeadlineError: If the new deadline is in the past.
        """
        _ , task_to_edit = self._get_task_by_id(task_id)
        
        if new_title is not None:
            if len(new_title) > 30:
                raise ValidationError("Task title cannot exceed 30 characters.")
            task_to_edit.title = new_title
        
        if new_description is not None:
            if len(new_description) > 150:
                raise ValidationError("Task description cannot exceed 150 characters.")
            task_to_edit.description = new_description
            
        if new_status is not None:
            task_to_edit.status = new_status
            
        if new_deadline is not None:
            if new_deadline < datetime.now():
                raise InvalidDeadlineError("Deadline cannot be in the past.")
            task_to_edit.deadline = new_deadline
        
        return task_to_edit

    def delete_task(self, task_id: int) -> None:
        """
        Deletes a task by its ID.

        :param task_id: The ID of the task to delete.
        :raises TaskNotFoundError: If the task with the given ID is not found.
        """
        parent_project, task_to_delete = self._get_task_by_id(task_id)
        parent_project.tasks.remove(task_to_delete)