# app/api/controllers/tasks_controller.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app.services import TaskService
from app.api.deps import get_task_service
from app.api.schemas.requests import TaskCreateRequest, TaskEditRequest
from app.api.schemas.responses import TaskResponse
from app.exceptions.service_exceptions import (
    TaskNotFoundError,
    ProjectNotFoundError,
    TaskLimitExceededError
)
from app.exceptions.base import ValidationError, InvalidDeadlineError

# We use two routers logically, but here we define endpoints explicitly
router = APIRouter(tags=["Tasks"])

# --- Nested Endpoints (Projects -> Tasks) ---

@router.get("/projects/{project_id}/tasks", response_model=List[TaskResponse])
def get_tasks_for_project(
    project_id: int,
    service: TaskService = Depends(get_task_service)
):
    """Get all tasks for a specific project."""
    try:
        return service.get_tasks_for_project(project_id)
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/projects/{project_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    project_id: int,
    data: TaskCreateRequest,
    service: TaskService = Depends(get_task_service)
):
    """Add a new task to a project."""
    try:
        # Since Pydantic converts date to datetime.date, but service might expect datetime or date,
        # we pass it directly. The service handles datetime conversion if needed.
        # But wait, our service uses `datetime` for deadline. Let's ensure compatibility.
        
        # Convert date to datetime if provided (midnight)
        deadline_dt = None
        if data.deadline:
            import datetime as dt
            deadline_dt = dt.datetime.combine(data.deadline, dt.time.min)

        return service.add_task_to_project(
            project_id=project_id,
            task_title=data.title,
            task_description=data.description,
            deadline=deadline_dt
        )
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (TaskLimitExceededError, ValidationError, InvalidDeadlineError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# --- Task Specific Endpoints ---

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    """Get a specific task details."""
    try:
        return service.find_task_by_id(task_id)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    data: TaskEditRequest,
    service: TaskService = Depends(get_task_service)
):
    """Update a task."""
    try:
        # Handle deadline conversion
        deadline_dt = None
        if data.deadline:
            import datetime as dt
            deadline_dt = dt.datetime.combine(data.deadline, dt.time.min)

        return service.edit_task(
            task_id,
            new_title=data.title,
            new_description=data.description,
            new_status=data.status,
            new_deadline=deadline_dt
        )
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (ValidationError, InvalidDeadlineError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    """Delete a task."""
    try:
        service.delete_task(task_id)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))