# app/main.py
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI

# Load .env variables
load_dotenv()

from app.api.routers import api_router
from app.db.session import get_session
from app.repositories import ProjectRepository, TaskRepository
from app.services import ProjectService, TaskService
from app.cli.console import CommandLineApp

# --- FastAPI Application Setup (Phase 3) ---

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle events for the application.
    This replaces the old 'on_event' startup/shutdown handlers.
    """
    # Startup: You can check DB connection here if needed
    print("🚀 ToDoList API is starting up...")
    yield
    # Shutdown: Cleanup code goes here
    print("🛑 ToDoList API is shutting down...")

app = FastAPI(
    title="ToDoList API",
    description="Phase 3: RESTful API for ToDoList Project using FastAPI",
    version="3.0.0",
    lifespan=lifespan
)

# Include the main API router
app.include_router(api_router, prefix="/api")


# --- Legacy CLI Entry Point (Deprecated) ---

def main():
    """
    Main entry point for the CLI application.
    WARNING: This interface is deprecated. Use 'uvicorn app.main:app' instead.
    """
    
    # Load configurations
    try:
        max_projects: int = int(os.getenv("MAX_PROJECTS", 10))
        max_tasks: int = int(os.getenv("MAX_TASKS_PER_PROJECT", 20))
    except (ValueError, TypeError):
        print("⚠️ Warning: Invalid .env config. Using default values.")
        max_projects, max_tasks = 10, 20

    # Create a database session for the CLI run
    session = get_session()

    try:
        # Initialize Repositories
        project_repo = ProjectRepository(session=session)
        task_repo = TaskRepository(session=session)

        # Initialize Services
        project_service = ProjectService(
            project_repo=project_repo, 
            max_projects=max_projects
        )
        task_service = TaskService(
            task_repo=task_repo,
            project_repo=project_repo,
            max_tasks_per_project=max_tasks,
        )

        # Initialize CLI
        cli_app = CommandLineApp(
            project_service=project_service, 
            task_service=task_service
        )

        print(
            f"Service initialized. Max projects: {max_projects}, "
            f"Max tasks per project: {max_tasks}. Using Database."
        )
        cli_app.run()

    except Exception as e:
        print(f"An unexpected error occurred during setup: {e}")
    finally:
        session.close()
        print("Database session closed.")


if __name__ == "__main__":
    main()