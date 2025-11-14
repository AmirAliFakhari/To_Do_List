# app/main.py
import os
from dotenv import load_dotenv

# Load .env variables (like DATABASE_URL and MAX_PROJECTS)
load_dotenv()

from app.db.session import get_session
from app.repositories import ProjectRepository, TaskRepository
from app.services import ProjectService, TaskService
from app.cli.console import CommandLineApp

def main():
    """
    Main entry point for the application.
    Sets up dependencies and runs the CLI.
    """
    
    # Load configurations
    try:
        max_projects: int = int(os.getenv("MAX_PROJECTS", 10))
        max_tasks: int = int(os.getenv("MAX_TASKS_PER_PROJECT", 20))
    except (ValueError, TypeError):
        print("⚠️ Warning: Invalid .env config. Using default values.")
        max_projects, max_tasks = 10, 20

    # 1. Create a single database session for this run
    # (For a web app, we'd do this per-request)
    session = get_session()

    try:
        # 2. Initialize Repositories
        project_repo = ProjectRepository(session=session)
        task_repo = TaskRepository(session=session)

        # 3. Initialize Services (injecting repositories)
        project_service = ProjectService(
            project_repo=project_repo, 
            max_projects=max_projects
        )
        task_service = TaskService(
            task_repo=task_repo,
            project_repo=project_repo,
            max_tasks_per_project=max_tasks,
        )

        # 4. Initialize CLI (injecting services)
        cli_app = CommandLineApp(
            project_service=project_service, 
            task_service=task_service
        )

        # 5. Run the application
        print(
            f"Service initialized. Max projects: {max_projects}, "
            f"Max tasks per project: {max_tasks}. Using Database."
        )
        cli_app.run()

    except Exception as e:
        print(f"An unexpected error occurred during setup: {e}")
    finally:
        # 6. Always close the session
        session.close()
        print("Database session closed.")


if __name__ == "__main__":
    main()