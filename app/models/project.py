# app/models/project.py
from __future__ import annotations
from typing import TYPE_CHECKING, List
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .task import Task

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, init=False)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(255))

    tasks: Mapped[List["Task"]] = relationship(
        "Task", 
        back_populates="project", 
        cascade="all, delete-orphan",
        init=False
    )