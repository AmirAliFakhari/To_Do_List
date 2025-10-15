# src/todolist/storage.py
"""
In-memory storage solution for the ToDoList application.
This class holds the data in memory and is responsible for managing IDs.
"""
from typing import List

from .models import Project


class InMemoryStorage:
    """Manages projects and tasks lists in memory."""

    def __init__(self):
        self.projects: List[Project] = []
        self._project_id_counter = 1
        self._task_id_counter = 1

    def get_next_project_id(self) -> int:
        """Returns the next available project ID and increments the counter."""
        project_id = self._project_id_counter
        self._project_id_counter += 1
        return project_id

    def get_next_task_id(self) -> int:
        """Returns the next available task ID and increments the counter."""
        task_id = self._task_id_counter
        self._task_id_counter += 1
        return task_id