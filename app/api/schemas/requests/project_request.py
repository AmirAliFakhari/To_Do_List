from typing import Optional
from pydantic import BaseModel, Field

class ProjectCreateRequest(BaseModel):
    """
    Schema for creating a new project.
    """
    name: str = Field(..., min_length=1, max_length=100, description="Unique name of the project")
    description: str = Field(..., min_length=1, max_length=255, description="Short description of the project")

class ProjectEditRequest(BaseModel):
    """
    Schema for editing an existing project.
    All fields are optional because user might want to update only one field.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=255)