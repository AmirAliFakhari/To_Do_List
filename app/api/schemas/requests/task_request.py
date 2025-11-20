from typing import Optional, Literal
from datetime import date
from pydantic import BaseModel, Field

# Define the allowed status types
StatusType = Literal["todo", "doing", "done"]

class TaskCreateRequest(BaseModel):
    """
    Schema for adding a task to a project.
    """
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    deadline: Optional[date] = Field(None, description="Deadline date (YYYY-MM-DD)")

class TaskEditRequest(BaseModel):
    """
    Schema for editing a task.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    status: Optional[StatusType] = Field(None, description="New status: todo, doing, or done")
    deadline: Optional[date] = Field(None)