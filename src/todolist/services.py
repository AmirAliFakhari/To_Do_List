# src/todolist/services.py

from datetime import datetime, timezone
from typing import Optional

from .exceptions import (
    InvalidDeadlineError,
    ProjectLimitExceededError,
    ProjectNameExistsError,
    ProjectNotFoundError,
    TaskLimitExceededError,
    TaskNotFoundError,
    ValidationError,
)
from .models import Project, Status, Task
from .storage import InMemoryStorage


class ToDoService:
    """
    Contains the main business logic for the ToDoList application.
    It is decoupled from the storage layer via Dependency Injection.
    """

    def __init__(
        self,
        storage: InMemoryStorage,
        max_projects: int,
        max_tasks_per_project: int,
    ):
        self._storage = storage
        self._max_projects = max_projects
        self._max_tasks_per_project = max_tasks_per_project

    # --- Helper Methods for Validation (Refactored to remove duplication) ---
    def _validate_project_fields(self, name: str, description: str) -> None:
        """Validates project name and description."""
        if len(name.split()) > 30:
            raise ValidationError("Project name cannot exceed 30 words.")
        if len(description.split()) > 150:
            raise ValidationError("Project description cannot exceed 150 words.")

    def _validate_task_fields(self, title: str, description: str) -> None:
        """Validates task title and description."""
        if len(title.split()) > 30:
            raise ValidationError("Task title cannot exceed 30 words.")
        if len(description.split()) > 150:
            raise ValidationError("Task description cannot exceed 150 words.")

    def _validate_deadline(self, deadline: Optional[datetime]):
        """Checks if the deadline is in the past (timezone-aware)."""
        if deadline:
            now_aware = datetime.now().astimezone()
            deadline_aware = (
                deadline.astimezone() if deadline.tzinfo else deadline
            )
            if deadline_aware.date() < now_aware.date():
                raise InvalidDeadlineError("Deadline cannot be in the past.")

    # --- Project Methods ---
    def create_project(self, name: str, description: str) -> Project:
        """Creates a new project."""
        projects = self._storage.projects
        if any(p.name.lower() == name.lower() for p in projects):
            raise ProjectNameExistsError(f"Project with name '{name}' already exists.")
        if len(projects) >= self._max_projects:
            raise ProjectLimitExceededError(f"Cannot create more than {self._max_projects} projects.")
        
        self._validate_project_fields(name, description)

        new_project = Project(
            id=self._storage.get_next_project_id(), name=name, description=description
        )
        projects.append(new_project)
        return new_project

    def edit_project(
        self,
        project_id: int,
        new_name: Optional[str] = None,
        new_description: Optional[str] = None,
    ) -> Project:
        """Edits an existing project."""
        project_to_edit = self.find_project_by_id(project_id)
        if not project_to_edit:
            raise ProjectNotFoundError(f"Project with ID '{project_id}' not found.")

        if new_name is not None:
            self._validate_project_fields(new_name, project_to_edit.description)
            if any(
                p.name.lower() == new_name.lower() and p.id != project_id
                for p in self._storage.projects
            ):
                raise ProjectNameExistsError(f"Another project with name '{new_name}' already exists.")
            project_to_edit.name = new_name

        if new_description is not None:
            self._validate_project_fields(project_to_edit.name, new_description)
            project_to_edit.description = new_description

        return project_to_edit

    def delete_project(self, project_id: int) -> None:
        """Deletes a project by its ID."""
        project_to_delete = self.find_project_by_id(project_id)
        if not project_to_delete:
            raise ProjectNotFoundError(f"Project with ID '{project_id}' not found.")
        self._storage.projects.remove(project_to_delete)

    def find_project_by_id(self, project_id: int) -> Optional[Project]:
        """Finds a project by its ID."""
        return next(
            (p for p in self._storage.projects if p.id == project_id), None
        )

    def get_all_projects(self) -> list[Project]:
        """Returns a list of all projects."""
        return self._storage.projects

    # --- Task Methods ---
    def add_task_to_project(
        self,
        project_id: int,
        task_title: str,
        task_description: str,
        deadline: Optional[datetime] = None,
    ) -> Task:
        """Adds a new task to a project."""
        project = self.find_project_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with ID '{project_id}' not found.")
        if len(project.tasks) >= self._max_tasks_per_project:
            raise TaskLimitExceededError(f"Cannot add more tasks to '{project.name}'.")

        self._validate_task_fields(task_title, task_description)
        self._validate_deadline(deadline)

        new_task = Task(
            id=self._storage.get_next_task_id(),
            title=task_title,
            description=task_description,
            deadline=deadline,
        )
        project.tasks.append(new_task)
        return new_task

    def find_task_by_id(self, task_id: int) -> Optional[Task]:
        """Finds a task by its ID across all projects."""
        for project in self._storage.projects:
            for task in project.tasks:
                if task.id == task_id:
                    return task
        return None
    
    def edit_task(
        self,
        task_id: int,
        new_title: Optional[str] = None,
        new_description: Optional[str] = None,
        new_status: Optional[Status] = None,
        new_deadline: Optional[datetime] = None,
    ) -> Task:
        """Edits an existing task."""
        task_to_edit = self.find_task_by_id(task_id)
        if not task_to_edit:
            raise TaskNotFoundError(f"Task with ID '{task_id}' not found.")

        if new_title is not None:
            self._validate_task_fields(new_title, task_to_edit.description)
            task_to_edit.title = new_title

        if new_description is not None:
            self._validate_task_fields(task_to_edit.title, new_description)
            task_to_edit.description = new_description

        if new_status is not None:
            task_to_edit.status = new_status

        if new_deadline is not None:
            self._validate_deadline(new_deadline)
            task_to_edit.deadline = new_deadline

        return task_to_edit

    def delete_task(self, task_id: int) -> None:
        """Deletes a task by its ID."""
        for project in self._storage.projects:
            task_to_delete = next((t for t in project.tasks if t.id == task_id), None)
            if task_to_delete:
                project.tasks.remove(task_to_delete)
                return
        raise TaskNotFoundError(f"Task with ID '{task_id}' not found.")