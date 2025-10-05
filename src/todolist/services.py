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
)

class ToDoService:
    """
    Contains the main business logic for the ToDoList application.
    It manages projects and tasks in memory.
    """
    def __init__(self, max_projects: int = 10, max_tasks_per_project: int = 20):
        self._projects: list[Project] = []
        self._max_projects = max_projects
        self._max_tasks_per_project = max_tasks_per_project
        # ID counters for auto-incrementing
        self._project_id_counter = 1
        self._task_id_counter = 1

    def create_project(self, name: str, description: str) -> Project:
        """Creates a new project and adds it to the list."""
        # Rule: Project name must be unique
        if any(p.name == name for p in self._projects):
            raise ProjectNameExistsError(f"Project with name '{name}' already exists.")

        # Rule: Cannot exceed the maximum number of projects
        if len(self._projects) >= self._max_projects:
            raise ProjectLimitExceededError(f"Cannot create more than {self._max_projects} projects.")

        # Rule: Validate input length
        if len(name) > 30:
            raise ValidationError("Project name cannot exceed 30 characters.")
        if len(description) > 150:
            raise ValidationError("Project description cannot exceed 150 characters.")

        # Assign an ID and create the project
        new_project = Project(id=self._project_id_counter, name=name, description=description)
        self._projects.append(new_project)
        self._project_id_counter += 1  # Increment the counter for the next project
        return new_project

    def get_all_projects(self) -> list[Project]:
        """Returns a list of all projects."""
        return self._projects

    def add_task_to_project(
        self,
        project_id: int,
        task_title: str,
        task_description: str,
        deadline: Optional[datetime] = None,
    ) -> Task:
        """Adds a new task to a specified project using its ID."""
        # Find the project by ID
        project = next((p for p in self._projects if p.id == project_id), None)
        if project is None:
            raise ProjectNotFoundError(f"Project with ID '{project_id}' not found.")

        # Rule: Cannot exceed the maximum number of tasks per project
        if len(project.tasks) >= self._max_tasks_per_project:
            raise TaskLimitExceededError(
                f"Cannot add more than {self._max_tasks_per_project} tasks to '{project.name}'."
            )

        # Rule: Validate input lengths
        if len(task_title) > 30:
            raise ValidationError("Task title cannot exceed 30 characters.")
        if len(task_description) > 150:
            raise ValidationError("Task description cannot exceed 150 characters.")

        # Assign an ID and create the task
        new_task = Task(
            id=self._task_id_counter,
            title=task_title,
            description=task_description,
            deadline=deadline,
        )
        project.tasks.append(new_task)
        self._task_id_counter += 1  # Increment the counter for the next task
        return new_task
    
    
    def change_task_status(self, task_id: int, new_status: Status) -> Task:
        """
        Finds a task by its ID across all projects and updates its status.
        """
        # Find the task with the given ID
        task_to_update = None
        for project in self._projects:
            for task in project.tasks:
                if task.id == task_id:
                    task_to_update = task
                    break
            if task_to_update:
                break
        
        if not task_to_update:
            raise TaskNotFoundError(f"Task with ID '{task_id}' not found.")
            
        # The 'Status' type hint already helps validate, but a runtime check is good practice
        # although in this case, Literal handles it. We'll proceed with the update.
        task_to_update.status = new_status
        return task_to_update
    
    
    def change_task_status(self, task_id: int, new_status: Status) -> Task:
        """Finds a task by its ID and updates its status."""
        task_to_update = None
        for project in self._projects:
            for task in project.tasks:
                if task.id == task_id:
                    task_to_update = task
                    break
            if task_to_update:
                break
        
        if not task_to_update:
            raise TaskNotFoundError(f"Task with ID '{task_id}' not found.")
            
        task_to_update.status = new_status
        return task_to_update

    def edit_task(
        self,
        task_id: int,
        new_title: Optional[str] = None,
        new_description: Optional[str] = None,
        new_deadline: Optional[datetime] = None,
    ) -> Task:
        """
        Finds a task by its ID and updates its details.
        Only non-None fields will be updated.
        """
        task_to_edit = None
        for project in self._projects:
            for task in project.tasks:
                if task.id == task_id:
                    task_to_edit = task
                    break
            if task_to_edit:
                break

        if not task_to_edit:
            raise TaskNotFoundError(f"Task with ID '{task_id}' not found.")

        # Update title if a new one is provided
        if new_title is not None:
            if len(new_title) > 30:
                raise ValidationError("Task title cannot exceed 30 characters.")
            task_to_edit.title = new_title

        # Update description if a new one is provided
        if new_description is not None:
            if len(new_description) > 150:
                raise ValidationError("Task description cannot exceed 150 characters.")
            task_to_edit.description = new_description
        
        # Update deadline if a new one is provided
        if new_deadline is not None:
            task_to_edit.deadline = new_deadline
            
        return task_to_edit
    
    
    def delete_task(self, task_id: int) -> None:
        """
        Finds a task by its ID and deletes it from its project.
        """
        parent_project = None
        task_to_delete = None

        for project in self._projects:
            for task in project.tasks:
                if task.id == task_id:
                    parent_project = project
                    task_to_delete = task
                    break
            if parent_project:
                break
        
        if not task_to_delete:
            raise TaskNotFoundError(f"Task with ID '{task_id}' not found.")

        parent_project.tasks.remove(task_to_delete)