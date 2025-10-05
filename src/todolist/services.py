# todolist/services.py

from .models import Project
from .exceptions import (
    ProjectNameExistsError,
    ProjectLimitExceededError,
    ValidationError,
)

class ToDoService:
    """
    This class contains the main business logic for the ToDoList application.
    It manages projects and tasks in memory.
    """
    def __init__(self, max_projects: int = 10):
        self._projects: list[Project] = []
        self._max_projects = max_projects # This will later come from a .env file

    def create_project(self, name: str, description: str) -> Project:
        """
        Creates a new project and adds it to the list.

        Raises:
            ProjectLimitExceededError: If the maximum number of projects is reached.
            ProjectNameExistsError: If a project with the same name already exists.
            ValidationError: If name or description exceed length limits.
        """
        # Rule: Cannot exceed the maximum number of projects [cite: 381]
        # Rule: Project name must be unique
        if any(p.name == name for p in self._projects):
            raise ProjectNameExistsError(f"Project with name '{name}' already exists.")

        # Rule: Cannot exceed the maximum number of projects
        if len(self._projects) >= self._max_projects:
            raise ProjectLimitExceededError(f"Cannot create more than {self._max_projects} projects.")




        # Rule: Validate input length [cite: 380]
        if len(name) > 30:
            raise ValidationError("Project name cannot exceed 30 characters.")
        if len(description) > 150:
            raise ValidationError("Project description cannot exceed 150 characters.")

        # If all rules pass, create and add the project
        new_project = Project(name=name, description=description)
        self._projects.append(new_project)
        return new_project

    def get_all_projects(self) -> list[Project]:
        """Returns a list of all projects."""
        return self._projects