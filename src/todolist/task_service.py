# src/todolist/task_service.py

from datetime import datetime, timezone
from typing import Optional

from .exceptions import (
    InvalidDeadlineError,
    ProjectNotFoundError,
    TaskLimitExceededError,
    TaskNotFoundError,
    ValidationError,
)
from .models import Project, Status, Task
from .storage import InMemoryStorage


class TaskService:
    """Handles business logic related to tasks."""

    def __init__(self, storage: InMemoryStorage, max_tasks_per_project: int):
        self._storage = storage
        self._max_tasks_per_project = max_tasks_per_project

    def _validate_fields(self, title: str, description: str) -> None:
        """Validates task title and description based on word count."""
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
        :param task_title: The title of the new task.
        :param task_description: The description of the new task.
        :param deadline: The optional deadline for the task.
        :return: The newly created Task object.
        :raises ProjectNotFoundError: If the project is not found.
        :raises TaskLimitExceededError: If the project has reached its task limit.
        :raises InvalidDeadlineError: If the deadline is in the past.
        """
        project = next(
            (p for p in self._storage.projects if p.id == project_id), None
        )
        if not project:
            raise ProjectNotFoundError(f"Project with ID '{project_id}' not found.")
        if len(project.tasks) >= self._max_tasks_per_project:
            raise TaskLimitExceededError(
                f"Cannot add more tasks to '{project.name}'."
            )

        self._validate_fields(task_title, task_description)
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
        """
        Finds a task by its unique ID across all projects.

        :param task_id: The ID of the task to find.
        :return: A Task object if found, otherwise None.
        """
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
        """
        Edits an existing task's attributes.

        :param task_id: The ID of the task to edit.
        :param new_title: The optional new title.
        :param new_description: The optional new description.
        :param new_status: The optional new status.
        :param new_deadline: The optional new deadline.
        :return: The updated Task object.
        :raises TaskNotFoundError: If the task is not found.
        """
        task_to_edit = self.find_task_by_id(task_id)
        if not task_to_edit:
            raise TaskNotFoundError(f"Task with ID '{task_id}' not found.")

        if new_title is not None:
            self._validate_fields(new_title, task_to_edit.description)
            task_to_edit.title = new_title

        if new_description is not None:
            self._validate_fields(task_to_edit.title, new_description)
            task_to_edit.description = new_description

        if new_status is not None:
            task_to_edit.status = new_status

        if new_deadline is not None:
            self._validate_deadline(new_deadline)
            task_to_edit.deadline = new_deadline

        return task_to_edit

    def delete_task(self, task_id: int) -> None:
        """
        Deletes a task by its ID.

        :param task_id: The ID of the task to delete.
        :raises TaskNotFoundError: If the task is not found.
        """
        for project in self._storage.projects:
            task_to_delete = next(
                (t for t in project.tasks if t.id == task_id), None
            )
            if task_to_delete:
                project.tasks.remove(task_to_delete)
                return
        raise TaskNotFoundError(f"Task with ID '{task_id}' not found.")