# app/api/controllers/projects_controller.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app.services import ProjectService
from app.api.deps import get_project_service
from app.api.schemas.requests import ProjectCreateRequest, ProjectEditRequest
from app.api.schemas.responses import ProjectResponse
from app.exceptions.service_exceptions import (
    ProjectNotFoundError,
    ProjectNameExistsError,
    ProjectLimitExceededError
)
from app.exceptions.base import ValidationError

# Define router
router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("/", response_model=List[ProjectResponse])
def get_all_projects(service: ProjectService = Depends(get_project_service)):
    """List all projects."""
    return service.get_all_projects()

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    data: ProjectCreateRequest,
    service: ProjectService = Depends(get_project_service)
):
    """Create a new project."""
    try:
        return service.create_project(data.name, data.description)
    except (ProjectNameExistsError, ProjectLimitExceededError, ValidationError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    service: ProjectService = Depends(get_project_service)
):
    """Get a specific project by ID."""
    try:
        return service.find_project_by_id(project_id)
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    data: ProjectEditRequest,
    service: ProjectService = Depends(get_project_service)
):
    """Update a project."""
    try:
        return service.edit_project(
            project_id,
            new_name=data.name,
            new_description=data.description
        )
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (ProjectNameExistsError, ValidationError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    service: ProjectService = Depends(get_project_service)
):
    """Delete a project."""
    try:
        service.delete_project(project_id)
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))