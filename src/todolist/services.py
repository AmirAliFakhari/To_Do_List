# src/todolist/services.py

from datetime import datetime
from typing import Optional

from .models import Project, Task
from .exceptions import (
    ProjectNameExistsError,
    ProjectLimitExceededError,
    ValidationError,
    ProjectNotFoundError,
    TaskLimitExceededError,
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