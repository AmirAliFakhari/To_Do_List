from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from .task_response import TaskResponse

class ProjectResponse(BaseModel):
    """
    Schema for sending project data to the client.
    """
    id: int
    name: str
    description: str
    
    # We can include tasks here if we want to show them inside the project
    # tasks: List[TaskResponse] = [] 

    model_config = ConfigDict(from_attributes=True)