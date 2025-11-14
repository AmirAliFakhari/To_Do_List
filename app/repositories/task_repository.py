# app/repositories/task_repository.py
from typing import Sequence, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models import Task, Project, Status

class TaskRepository:
    def __init__(self, session: Session):
        """
        Initialize the repository with a database session.
        """
        self.session = session

    def create(
        self,
        project: Project,
        title: str,
        description: str,
        deadline: Optional[datetime] = None,
    ) -> Task:
        """
        Create a new task and associate it with a project.
        """
        # Create the task instance
        db_task = Task(
            title=title, 
            description=description, 
            deadline=deadline
        )
        
        # Add it to the project's list of tasks
        # SQLAlchemy will automatically handle setting the project_id
        project.tasks.append(db_task)
        
        self.session.commit()
        self.session.refresh(db_task)
        return db_task

    def get_by_id(self, task_id: int) -> Task | None:
        """
        Get a single task by its ID.
        """
        return self.session.get(Task, task_id)

    def get_tasks_for_project(self, project_id: int) -> Sequence[Task]:
        """
        Get all tasks associated with a specific project ID, sorted by task ID.
        """
        statement = (
            select(Task)
            .where(Task.project_id == project_id)
            .order_by(Task.id)
        )
        return self.session.scalars(statement).all()

    def update(
        self,
        task: Task,
        new_title: Optional[str] = None,
        new_description: Optional[str] = None,
        new_status: Optional[Status] = None,
        new_deadline: Optional[datetime] = None,
    ) -> Task:
        """
        Update a task's details.
        """
        if new_title is not None:
            task.title = new_title
        if new_description is not None:
            task.description = new_description
        if new_status is not None:
            task.status = new_status
        if new_deadline is not None:
            task.deadline = new_deadline
        
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        """
        Delete a task.
        """
        self.session.delete(task)
        self.session.commit()