# src/todolist/exceptions.py

class ToDoListError(Exception):
    """Base exception class for this application."""
    pass

class ProjectNameExistsError(ToDoListError):
    """Raised when trying to create a project with a name that already exists."""
    pass

class ProjectLimitExceededError(ToDoListError):
    """Raised when the maximum number of projects has been reached."""
    pass

class TaskLimitExceededError(ToDoListError):
    """Raised when the maximum number of tasks for a project has been reached."""
    pass

class ValidationError(ToDoListError):
    """Raised for general validation errors, like incorrect length."""
    pass

class ProjectNotFoundError(ToDoListError):
    """Raised when a project is not found by its name or ID."""
    pass

class TaskNotFoundError(ToDoListError):
    """Raised when a task is not found by its ID."""
    pass

class InvalidDeadlineError(ValidationError):
    """Raised when the provided deadline is in the past."""
    pass

