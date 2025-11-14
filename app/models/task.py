# app/models/task.py
from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .project import Project

# (Status از فایل قبلی را اینجا می‌آوریم)
from typing import Literal
Status = Literal["todo", "doing", "done"]

class Task(Base):
    __tablename__ = "tasks"

    # ستون‌های جدول
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, init=False)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500))
    deadline: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    status: Mapped[Status] = mapped_column(String(50), default="todo")
    
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        init=False
    )
    
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"), init=False)

    project: Mapped["Project"] = relationship(
        "Project", 
        back_populates="tasks",
        init=False
    )