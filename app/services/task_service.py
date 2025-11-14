from datetime import datetime
from typing import Optional, Sequence

from app.models import Project, Task
from app.models.task import Status
from app.repositories import ProjectRepository, TaskRepository  # <-- This is the key line
from app.exceptions.base import InvalidDeadlineError, ValidationError
from app.exceptions.service_exceptions import (
    ProjectNotFoundError,
    TaskLimitExceededError,
    TaskNotFoundError,
)
class TaskService:
    """Handles business logic related to tasks."""

    def __init__(
        self,
        task_repo: TaskRepository,
        project_repo: ProjectRepository,
        max_tasks_per_project: int,
    ):
        """
        Initialize the service with repositories and configurations.
        """
        self._task_repo = task_repo
        self._project_repo = project_repo
        self._max_tasks_per_project = max_tasks_per_project

    def _validate_fields(
        self, title: str, description: str, status: Optional[Status] = None
    ) -> None:
        """Validates all task fields based on DB constraints."""
        if not title or not title.strip():
            raise ValidationError("Task title cannot be empty.")
        if not description or not description.strip():
            raise ValidationError("Task description cannot be empty.")
        
        # Updated validation to match DB schema
        if len(title) > 100:
            raise ValidationError("Task title cannot exceed 100 characters.")
        if len(description) > 500:
            raise ValidationError("Task description cannot exceed 500 characters.")
        
        if status and status not in ["todo", "doing", "done"]:
            raise ValidationError("Status must be one of 'todo', 'doing', or 'done'.")

    def _validate_deadline(self, deadline: Optional[datetime]):
        """Checks if the deadline is in the past."""
        if deadline:
            # Ensure deadline is timezone-aware if it's not already
            deadline_aware = (
                deadline.astimezone() if deadline.tzinfo is None else deadline
            )
            # Ensure now is timezone-aware
            now_aware = datetime.now().astimezone()

            if deadline_aware.date() < now_aware.date():
                raise InvalidDeadlineError("Deadline cannot be in the past.")

    def add_task_to_project(
        self,
        project_id: int,
        task_title: str,
        task_description: str,
        deadline: Optional[datetime] = None,
    ) -> Task:
        """Adds a new task to a project."""
        self._validate_fields(task_title, task_description)
        self._validate_deadline(deadline)

        # Find the project using the repository
        project = self._project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with ID '{project_id}' not found.")
        
        # Check task limit (accessing the relationship)
        if len(project.tasks) >= self._max_tasks_per_project:
            raise TaskLimitExceededError(
                f"Cannot add more tasks to '{project.name}'."
            )

        # Create the task using the repository
        return self._task_repo.create(
            project=project,
            title=task_title,
            description=task_description,
            deadline=deadline,
        )

    def find_task_by_id(self, task_id: int) -> Task:
        """Finds a task by its ID. Raises error if not found."""
        task = self._task_repo.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID '{task_id}' not found.")
        return task

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

        title_to_validate = new_title if new_title is not None else task_to_edit.title
        desc_to_validate = (
            new_description if new_description is not None else task_to_edit.description
        )
        status_to_validate = (
            new_status if new_status is not None else task_to_edit.status
        )
        self._validate_fields(title_to_validate, desc_to_validate, status_to_validate)

        if new_deadline is not None:
            self._validate_deadline(new_deadline)

        # Update the task using the repository
        return self._task_repo.update(
            task=task_to_edit,
            new_title=new_title,
            new_description=new_description,
            new_status=new_status,
            new_deadline=new_deadline,
        )

    def delete_task(self, task_id: int) -> None:
        """Deletes a task by its ID."""
        task_to_delete = self.find_task_by_id(task_id)
        # Delete the task using the repository
        self._task_repo.delete(task_to_delete)

    def get_tasks_for_project(self, project_id: int) -> Sequence[Task]:
        """Gets all tasks for a specific project."""
        # First, ensure project exists
        if not self._project_repo.get_by_id(project_id):
            raise ProjectNotFoundError(f"Project with ID '{project_id}' not found.")
        
        return self._task_repo.get_tasks_for_project(project_id)