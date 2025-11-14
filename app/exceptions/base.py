# app/exceptions/base.py
class ToDoListError(Exception):
    """Base exception class for this application."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class ValidationError(ToDoListError):
    """Raised for general validation errors."""
    pass

class InvalidDeadlineError(ValidationError):
    """Raised when the provided deadline is in the past."""
    pass