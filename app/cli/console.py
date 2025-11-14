# app/cli/console.py
import os
import sys
from datetime import datetime
from typing import List, Optional, Sequence

from app.models import Project, Task, Status
from app.services import ProjectService, TaskService
from app.exceptions.base import ToDoListError

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

class CommandLineApp:
    def __init__(self, project_service: ProjectService, task_service: TaskService):
        """
        Initialize the CLI app with injected services.
        """
        self.project_service = project_service
        self.task_service = task_service

    def _print_menu(self):
        """Prints the main menu options."""
        print("\n--- ToDoList Menu (Phase 2: RDB) ---")
        print("1. Create a new project")
        print("2. List all projects")
        print("3. Edit a project")
        print("4. Delete a project")
        print("5. Add a task to a project")
        print("6. Edit a task")
        print("7. Delete a task")
        print("8. List tasks for a project")
        print("0. Exit")

    def run(self):
        """Main function to run the robust CLI application."""
        while True:
            self._print_menu()
            choice: str = input("Enter your choice: ").strip()

            try:
                if choice == "1":
                    self._create_project()
                elif choice == "2":
                    self._list_all_projects()
                elif choice == "3":
                    self._edit_project()
                elif choice == "4":
                    self._delete_project()
                elif choice == "5":
                    self._add_task_to_project()
                elif choice == "6":
                    self._edit_task()
                elif choice == "7":
                    self._delete_task()
                elif choice == "8":
                    self._list_tasks_for_project()
                elif choice == "0":
                    print("Exiting application. Goodbye!")
                    break
                else:
                    print("❌ ERROR: Invalid choice. Please try again.")

            except ToDoListError as e:
                print(f"❌ ERROR: {e.message}")
            except ValueError:
                print("❌ ERROR: Invalid input. Please enter a valid number for IDs.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    # --- Helper Methods for each choice ---

    def _create_project(self):
        name: str = input("Enter project name: ").strip()
        description: str = input("Enter project description: ").strip()
        project: Project = self.project_service.create_project(name, description)
        print(f"✅ SUCCESS: Project '{project.name}' created with ID {project.id}.")

    def _list_all_projects(self):
        projects: Sequence[Project] = self.project_service.get_all_projects()
        if not projects:
            print("No projects found.")
        else:
            print("\n--- All Projects ---")
            for project in projects:
                print(
                    f"- ID: {project.id}, Name: {project.name}, Tasks: {len(project.tasks)}"
                )
                print(f"  Description: {project.description}")

    def _edit_project(self):
        project_id_str: str = input("Enter project ID to edit: ").strip()
        project_id: int = int(project_id_str)

        new_name: str = input("New name (leave blank to keep): ").strip()
        new_description: str = input("New description (leave blank to keep): ").strip()

        if not new_name and not new_description:
            print("💡 INFO: No changes were made.")
            return

        updated_project: Project = self.project_service.edit_project(
            project_id,
            new_name=new_name or None,
            new_description=new_description or None,
        )
        print(f"✅ SUCCESS: Project {updated_project.id} updated.")

    def _delete_project(self):
        project_id_str: str = input("Enter project ID to delete: ").strip()
        project_id: int = int(project_id_str)
        self.project_service.delete_project(project_id)
        print(f"✅ SUCCESS: Project with ID {project_id} deleted.")

    def _add_task_to_project(self):
        project_id_str: str = input("Enter project ID to add task to: ").strip()
        project_id: int = int(project_id_str)
        
        # We call the service to ensure the project exists before asking for task details
        _ = self.project_service.find_project_by_id(project_id)
        
        title: str = input("Enter task title: ").strip()
        description: str = input("Enter task description: ").strip()
        deadline_str: str = input("Deadline (YYYY-MM-DD) [optional]: ").strip()

        deadline: Optional[datetime] = None
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
            except ValueError:
                print("❌ ERROR: Invalid date format. Please use YYYY-MM-DD.")
                return

        task: Task = self.task_service.add_task_to_project(
            project_id, title, description, deadline
        )
        print(f"✅ SUCCESS: Task '{task.title}' added to project ID {project_id}.")

    def _edit_task(self):
        task_id_str: str = input("Enter task ID to edit: ").strip()
        task_id: int = int(task_id_str)

        # We find the task first to ensure it exists
        _ = self.task_service.find_task_by_id(task_id)

        new_title: str = input("New title (leave blank to keep): ").strip()
        new_desc: str = input("New description (leave blank to keep): ").strip()
        new_status: str = input("New status (todo/doing/done) [blank to keep]: ").strip()
        new_deadline_str: str = input("New deadline (YYYY-MM-DD) [blank to keep]: ").strip()

        if not any([new_title, new_desc, new_status, new_deadline_str]):
            print("💡 INFO: No changes were made.")
            return

        t_deadline: Optional[datetime] = None
        if new_deadline_str:
            try:
                t_deadline = datetime.strptime(new_deadline_str, "%Y-%m-%d")
            except ValueError:
                print("❌ ERROR: Invalid date format. Please use YYYY-MM-DD.")
                return

        task: Task = self.task_service.edit_task(
            task_id,
            new_title=new_title or None,
            new_description=new_desc or None,
            new_status=new_status or None, # type: ignore
            new_deadline=t_deadline,
        )
        print(f"✅ SUCCESS: Task {task.id} updated.")

    def _delete_task(self):
        task_id_str: str = input("Enter task ID to delete: ").strip()
        task_id: int = int(task_id_str)
        self.task_service.delete_task(task_id)
        print(f"✅ SUCCESS: Task with ID {task_id} deleted.")

    def _list_tasks_for_project(self):
        project_id_str: str = input("Enter project ID to list tasks for: ").strip()
        project_id: int = int(project_id_str)
        
        # We get the project first to show its name
        project: Project = self.project_service.find_project_by_id(project_id)
        tasks: Sequence[Task] = self.task_service.get_tasks_for_project(project_id)

        if not tasks:
            print(f"No tasks found for project '{project.name}'.")
        else:
            print(f"\n--- Tasks for Project: {project.name} ---")
            for task in tasks:
                deadline_info = (
                    task.deadline.strftime("%Y-%m-%d")
                    if task.deadline
                    else "No deadline"
                )
                print(
                    f"- ID: {task.id}, Title: {task.title}, "
                    f"Status: {task.status}, Deadline: {deadline_info}"
                )