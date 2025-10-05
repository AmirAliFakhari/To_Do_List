# todolist/models.py

from dataclasses import dataclass, field
from typing import Literal, Optional
from datetime import datetime

# Define a specific type for task statuses for better type checking
Status = Literal["todo", "doing", "done"]

@dataclass
class Task:
    """Represents a single task within a project."""
    title: str
    description: str
    status: Status = "todo"  # Default status is 'todo' [cite: 86]
    deadline: Optional[datetime] = None
    # We will add an ID later when we need to uniquely identify tasks.

@dataclass
class Project:
    """Represents a project that contains a collection of tasks."""
    name: str
    description: str
    tasks: list[Task] = field(default_factory=list)
    # We will add an ID later as well.