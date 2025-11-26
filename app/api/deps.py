# app/api/deps.py
import os
from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories import ProjectRepository, TaskRepository
from app.services import ProjectService, TaskService

def get_db() -> Generator[Session, None, None]:
    """
    Creates a new database session for each request and closes it afterwards.
    """
    db = get_session()
    try:
        yield db
    finally:
        db.close()

def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    repo = ProjectRepository(db)
    max_projects = int(os.getenv("MAX_PROJECTS", 10))
    return ProjectService(repo, max_projects)

def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    project_repo = ProjectRepository(db)
    task_repo = TaskRepository(db)
    max_tasks = int(os.getenv("MAX_TASKS_PER_PROJECT", 20))
    return TaskService(task_repo, project_repo, max_tasks)