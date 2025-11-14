# app/db/base.py
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

class Base(DeclarativeBase, MappedAsDataclass):
    """
    Base class for all SQLAlchemy models in the application.
    Inherits from MappedAsDataclass to provide dataclass-like behaviors.
    """
    pass