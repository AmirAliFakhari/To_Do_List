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

    def __init__(self, max_projects: int = 10, max_tasks_per_project: int = 20):
        self._projects: list[Project] = []
        self._max_projects = max_projects
        self._max_tasks_per_project = max_tasks_per_project 

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

        new_project = Project(name=name, description=description)
        self._projects.append(new_project)
        return new_project

    def get_all_projects(self) -> list[Project]:
        """Returns a list of all projects."""
        return self._projects

    def add_task_to_project(
        self,
        project_name: str,
        task_title: str,
        task_description: str,
        deadline: Optional[datetime] = None,
    ) -> Task:
        """Adds a new task to a specified project."""
        project = next((p for p in self._projects if p.name == project_name), None)
        if project is None:
            raise ProjectNotFoundError(f"Project with name '{project_name}' not found.")

        if len(project.tasks) >= self._max_tasks_per_project:
            raise TaskLimitExceededError(
                f"Cannot add more than {self._max_tasks_per_project} tasks to '{project_name}'."
            )

        if len(task_title) > 30:
            raise ValidationError("Task title cannot exceed 30 characters.")
        if len(task_description) > 150:
            raise ValidationError("Task description cannot exceed 150 characters.")

        new_task = Task(title=task_title, description=task_description, deadline=deadline)
        project.tasks.append(new_task)
        return new_task