from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel, ConfigDict

StatusType = Literal["todo", "doing", "done"]

class TaskResponse(BaseModel):
    """
    Schema for sending task data to the client.
    """
    id: int
    title: str
    description: str
    status: StatusType
    deadline: Optional[datetime] = None
    created_at: datetime
    closed_at: Optional[datetime] = None
    project_id: int

    # This allows Pydantic to read data directly from SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)