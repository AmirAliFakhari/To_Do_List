# src/todolist/project_service.py

from typing import List, Optional

from .exceptions import (
    ProjectLimitExceededError,
    ProjectNameExistsError,
    ProjectNotFoundError,
    ValidationError,
)
from .models import Project
from .storage import InMemoryStorage


class ProjectService:
    """Handles business logic related to projects."""

    def __init__(self, storage: InMemoryStorage, max_projects: int):
        self._storage = storage
        self._max_projects = max_projects

    def _validate_fields(self, name: str, description: str) -> None:
        """Validates project name and description based on word count."""
        if len(name.split()) > 30:
            raise ValidationError("Project name cannot exceed 30 words.")
        if len(description.split()) > 150:
            raise ValidationError("Project description cannot exceed 150 words.")

    def create_project(self, name: str, description: str) -> Project:
        """Creates a new project."""
        projects = self._storage.projects
        if any(p.name.lower() == name.lower() for p in projects):
            raise ProjectNameExistsError(
                f"Project with name '{name}' already exists (case-insensitive)."
            )
        if len(projects) >= self._max_projects:
            raise ProjectLimitExceededError(
                f"Cannot create more than {self._max_projects} projects."
            )

        self._validate_fields(name, description)

        new_project = Project(
            id=self._storage.get_next_project_id(), name=name, description=description
        )
        projects.append(new_project)
        return new_project

    def find_project_by_id(self, project_id: int) -> Optional[Project]:
        """Finds a project by its ID."""
        return next(
            (p for p in self._storage.projects if p.id == project_id), None
        )

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
            self._validate_fields(new_name, project_to_edit.description)
            if any(
                p.name.lower() == new_name.lower() and p.id != project_id
                for p in self._storage.projects
            ):
                raise ProjectNameExistsError(
                    f"Another project with name '{new_name}' already exists."
                )
            project_to_edit.name = new_name

        if new_description is not None:
            self._validate_fields(project_to_edit.name, new_description)
            project_to_edit.description = new_description

        return project_to_edit

    def delete_project(self, project_id: int) -> None:
        """Deletes a project by its ID."""
        project_to_delete = self.find_project_by_id(project_id)
        if not project_to_delete:
            raise ProjectNotFoundError(f"Project with ID '{project_id}' not found.")
        self._storage.projects.remove(project_to_delete)

    def get_all_projects(self) -> List[Project]:
        """Returns a list of all projects."""
        return self._storage.projects