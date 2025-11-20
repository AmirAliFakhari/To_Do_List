# app/exceptions/service_exceptions.py
from .base import ToDoListError

class ProjectNameExistsError(ToDoListError):
    """Raised when trying to create a project with a name that already exists."""
    pass

class ProjectLimitExceededError(ToDoListError):
    """Raised when the maximum number of projects has been reached."""
    pass

class TaskLimitExceededError(ToDoListError):
    """Raised when the maximum number of tasks for a project has been reached."""
    pass

class ProjectNotFoundError(ToDoListError):
    """Raised when a project is not found by its ID."""
    pass

class TaskNotFoundError(ToDoListError):
    """Raised when a task is not found by its ID."""
    pass