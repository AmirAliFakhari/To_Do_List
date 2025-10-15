# main.py
import os
import sys
from datetime import datetime
from typing import List, Optional

from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from todolist.exceptions import ToDoListError
from todolist.models import Project, Task
from todolist.project_service import ProjectService
from todolist.storage import InMemoryStorage
from todolist.task_service import TaskService


def print_menu():
    """Prints the main menu options."""
    print("\n--- ToDoList Menu ---")
    print("1. Create a new project")
    print("2. List all projects")
    print("3. Edit a project")
    print("4. Delete a project")
    print("5. Add a task to a project")
    print("6. Edit a task")
    print("7. Delete a task")
    print("8. List tasks for a project")
    print("0. Exit")


def main():
    """Main function to run the robust CLI application."""
    load_dotenv()
    try:
        max_projects: int = int(os.getenv("MAX_PROJECTS", 10))
        max_tasks: int = int(os.getenv("MAX_TASKS_PER_PROJECT", 20))
    except (ValueError, TypeError):
        print("⚠️ Warning: Invalid .env config. Using default values.")
        max_projects, max_tasks = 10, 20

    storage = InMemoryStorage()
    project_service = ProjectService(storage=storage, max_projects=max_projects)
    task_service = TaskService(storage=storage, max_tasks_per_project=max_tasks)

    print(
        f"Service initialized. Max projects: {max_projects}, "
        f"Max tasks per project: {max_tasks}"
    )

    while True:
        print_menu()
        choice: str = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                name: str = input("Enter project name: ").strip()
                description: str = input("Enter project description: ").strip()
                project: Project = project_service.create_project(name, description)
                print(f"✅ SUCCESS: Project '{project.name}' created with ID {project.id}.")

            elif choice == "2":
                projects: List[Project] = project_service.get_all_projects()
                if not projects:
                    print("No projects found.")
                else:
                    print("\n--- All Projects ---")
                    for project in projects:
                        print(f"- ID: {project.id}, Name: {project.name}, Tasks: {len(project.tasks)}")
                        print(f"  Description: {project.description}")

            elif choice == "3":
                project_id_str: str = input("Enter project ID to edit: ").strip()
                project_id: int = int(project_id_str)

                new_name: str = input("New name (leave blank to keep): ").strip()
                new_description: str = input("New description (leave blank to keep): ").strip()

                if not new_name and not new_description:
                    print("💡 INFO: No changes were made.")
                    continue

                updated_project: Project = project_service.edit_project(
                    project_id,
                    new_name=new_name or None,
                    new_description=new_description or None,
                )
                print(f"✅ SUCCESS: Project {updated_project.id} updated.")

            elif choice == "4":
                project_id_str: str = input("Enter project ID to delete: ").strip()
                project_id: int = int(project_id_str)
                project_service.delete_project(project_id)
                print(f"✅ SUCCESS: Project with ID {project_id} deleted.")

            elif choice == "5":
                project_id_str: str = input("Enter project ID to add task to: ").strip()
                project_id: int = int(project_id_str)
                
                title: str = input("Enter task title: ").strip()
                description: str = input("Enter task description: ").strip()
                deadline_str: str = input("Deadline (YYYY-MM-DD) [optional]: ").strip()

                deadline: Optional[datetime] = None
                if deadline_str:
                    try:
                        deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
                    except ValueError:
                        print("❌ ERROR: Invalid date format. Please use YYYY-MM-DD.")
                        continue

                task: Task = task_service.add_task_to_project(
                    project_id, title, description, deadline
                )
                print(f"✅ SUCCESS: Task '{task.title}' added to project ID {project_id}.")

            elif choice == "6":
                task_id_str: str = input("Enter task ID to edit: ").strip()
                task_id: int = int(task_id_str)

                new_title: str = input("New title (leave blank to keep): ").strip()
                new_desc: str = input("New description (leave blank to keep): ").strip()
                new_status: str = input("New status (todo/doing/done) [blank to keep]: ").strip()
                new_deadline_str: str = input("New deadline (YYYY-MM-DD) [blank to keep]: ").strip()

                if not any([new_title, new_desc, new_status, new_deadline_str]):
                    print("💡 INFO: No changes were made.")
                    continue

                t_deadline: Optional[datetime] = None
                if new_deadline_str:
                    try:
                        t_deadline = datetime.strptime(new_deadline_str, "%Y-%m-%d")
                    except ValueError:
                        print("❌ ERROR: Invalid date format. Please use YYYY-MM-DD.")
                        continue

                task: Task = task_service.edit_task(
                    task_id,
                    new_title=new_title or None,
                    new_description=new_desc or None,
                    new_status=new_status or None,
                    new_deadline=t_deadline,
                )
                print(f"✅ SUCCESS: Task {task.id} updated.")

            elif choice == "7":
                task_id_str: str = input("Enter task ID to delete: ").strip()
                task_id: int = int(task_id_str)
                task_service.delete_task(task_id)
                print(f"✅ SUCCESS: Task with ID {task_id} deleted.")

            elif choice == "8":
                project_id_str: str = input("Enter project ID to list tasks for: ").strip()
                project_id: int = int(project_id_str)
                
                project: Optional[Project] = project_service.find_project_by_id(project_id)

                if not project:
                    print(f"❌ ERROR: Project with ID {project_id} not found.")
                elif not project.tasks:
                    print(f"No tasks found for project '{project.name}'.")
                else:
                    print(f"\n--- Tasks for Project: {project.name} ---")
                    sorted_tasks = sorted(project.tasks, key=lambda t: t.id)
                    for task in sorted_tasks:
                        deadline_info = (
                            task.deadline.strftime("%Y-%m-%d")
                            if task.deadline
                            else "No deadline"
                        )
                        print(f"- ID: {task.id}, Title: {task.title}, Status: {task.status}, Deadline: {deadline_info}")

            elif choice == "0":
                print("Exiting application. Goodbye!")
                break
            else:
                print("❌ ERROR: Invalid choice. Please try again.")

        except ToDoListError as e:
            print(f"❌ ERROR: {e}")
        except ValueError:
            print("❌ ERROR: Invalid input. Please enter a valid number for IDs.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()