# app/repositories/project_repository.py
from typing import List, Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session



from app.models import Project

class ProjectRepository:
    def __init__(self, session: Session):
        """
        Initialize the repository with a database session.
        """
        self.session = session

    def create(self, name: str, description: str) -> Project:
        """
        Create a new project.
        """
        # We use init=False on relationships, so we pass
        # model fields explicitly.
        db_project = Project(name=name, description=description)
        self.session.add(db_project)
        self.session.commit()
        self.session.refresh(db_project)
        return db_project

    def get_by_id(self, project_id: int) -> Project | None:
        """
        Get a single project by its ID.
        """
        # .get() is the simplest way to fetch by primary key
        return self.session.get(Project, project_id)

    def get_by_name(self, name: str) -> Project | None:
        """
        Get a single project by its name (case-insensitive).
        """
        statement = select(Project).where(Project.name.ilike(name))
        return self.session.scalars(statement).first()

    def get_all(self) -> Sequence[Project]:
        """
        Get all projects, sorted by ID.
        """
        statement = select(Project).order_by(Project.id)
        return self.session.scalars(statement).all()
    
    def count(self) -> int:
        """
        Get the total number of projects.
        """
        return len(self.session.scalars(select(Project)).all())

    def update(
        self, 
        project: Project, 
        new_name: str | None = None, 
        new_description: str | None = None
    ) -> Project:
        """
        Update a project's details.
        """
        if new_name:
            project.name = new_name
        if new_description:
            project.description = new_description
        
        self.session.commit()
        self.session.refresh(project)
        return project

    def delete(self, project: Project) -> None:
        """
        Delete a project.
        """
        self.session.delete(project)
        self.session.commit()