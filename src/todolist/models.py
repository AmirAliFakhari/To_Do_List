# src/todolist/models.py

from dataclasses import dataclass, field
from typing import Literal, Optional
from datetime import datetime

# Define a specific type for task statuses for better type checking
Status = Literal["todo", "doing", "done"]

@dataclass
class Task:
    """Represents a single task within a project."""
    title: str
    id: int
    description: str
    status: Status = "todo"  # Default status is 'todo'
    deadline: Optional[datetime] = None

@dataclass
class Project:
    """Represents a project that contains a collection of tasks."""
    name: str
    id: int
    description: str
    tasks: list[Task] = field(default_factory=list)