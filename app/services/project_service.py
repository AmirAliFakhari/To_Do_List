# app/services/project_service.py
from typing import Optional, Sequence

from app.repositories import ProjectRepository
from app.models import Project
from app.exceptions.service_exceptions import (
    ProjectLimitExceededError,
    ProjectNameExistsError,
    ProjectNotFoundError,
    ValidationError,
)

class ProjectService:
    """Handles business logic related to projects."""

    def __init__(self, project_repo: ProjectRepository, max_projects: int):
        """
        Initialize the service with a repository and configurations.
        """
        self._repo = project_repo
        self._max_projects = max_projects

    def _validate_fields(self, name: str, description: str) -> None:
        """Validates project fields."""
        if not name or not name.strip():
            raise ValidationError("Project name cannot be empty.")
        if not description or not description.strip():
            raise ValidationError("Project description cannot be empty.")
        if len(name) > 100:
            raise ValidationError("Project name cannot exceed 100 characters.")
        if len(description) > 255:
            raise ValidationError("Project description cannot exceed 255 characters.")

    def create_project(self, name: str, description: str) -> Project:
        """Creates a new project."""
        self._validate_fields(name, description)
        
        # Check for duplicate name (using the repository)
        if self._repo.get_by_name(name):
            raise ProjectNameExistsError(
                f"Project with name '{name}' already exists (case-insensitive)."
            )
        
        # Check project limit (using the repository)
        if self._repo.count() >= self._max_projects:
            raise ProjectLimitExceededError(
                f"Cannot create more than {self._max_projects} projects."
            )

        # Create project (using the repository)
        return self._repo.create(name=name, description=description)

    def find_project_by_id(self, project_id: int) -> Project:
        """Finds a project by its ID. Raises error if not found."""
        project = self._repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with ID '{project_id}' not found.")
        return project

    def edit_project(
        self,
        project_id: int,
        new_name: Optional[str] = None,
        new_description: Optional[str] = None,
    ) -> Project:
        """Edits an existing project."""
        project_to_edit = self.find_project_by_id(project_id)

        name_to_validate = new_name if new_name is not None else project_to_edit.name
        desc_to_validate = (
            new_description if new_description is not None else project_to_edit.description
        )
        self._validate_fields(name_to_validate, desc_to_validate)

        if new_name is not None and new_name.lower() != project_to_edit.name.lower():
            # Check if the *new* name already exists
            if self._repo.get_by_name(new_name):
                raise ProjectNameExistsError(
                    f"Another project with name '{new_name}' already exists."
                )

        # Update project (using the repository)
        return self._repo.update(
            project=project_to_edit,
            new_name=new_name,
            new_description=new_description,
        )

    def delete_project(self, project_id: int) -> None:
        """Deletes a project by its ID."""
        project_to_delete = self.find_project_by_id(project_id)
        # Delete project (using the repository)
        self._repo.delete(project_to_delete)

    def get_all_projects(self) -> Sequence[Project]:
        """Returns a sequence of all projects."""
        return self._repo.get_all()