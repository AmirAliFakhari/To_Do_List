# main.py

import os
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv

from src.todolist.services import ToDoService
from src.todolist.models import Project, Task
from src.todolist.exceptions import ToDoListError

# --- Helper Functions for User Input ---

def get_non_empty_input(prompt: str) -> str:
    """Gets a non-empty string input from the user."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("❌ ERROR: Input cannot be empty. Please try again.")

def get_int_input(prompt: str) -> int:
    """Gets a valid integer input from the user."""
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("❌ ERROR: Invalid input. Please enter a valid number.")

# --- Handler Functions for Menu Choices ---

def handle_create_project(service: ToDoService):
    """Handles the logic for creating a new project."""
    name = get_non_empty_input("Enter project name: ")
    description = input("Enter project description: ").strip()
    project = service.create_project(name, description)
    print(f"✅ SUCCESS: Project '{project.name}' created with ID {project.id}.")

def handle_list_projects(service: ToDoService):
    """Handles the logic for listing all projects."""
    projects = service.get_all_projects()
    if not projects:
        print("No projects found.")
    else:
        print("\n--- All Projects ---")
        for project in projects:
            print(f"- ID: {project.id}, Name: {project.name}, Tasks: {len(project.tasks)}")
            print(f"  Description: {project.description}")

def handle_edit_project(service: ToDoService):
    """Handles the logic for editing a project."""
    project_id = get_int_input("Enter project ID to edit: ")
    new_name = input("New name (leave blank to keep): ").strip()
    new_description = input("New description (leave blank to keep): ").strip()

    if not new_name and not new_description:
        print("💡 INFO: No changes were made.")
        return

    updated_project = service.edit_project(
        project_id,
        new_name=new_name or None,
        new_description=new_description or None
    )
    print(f"✅ SUCCESS: Project {updated_project.id} updated.")

def handle_delete_project(service: ToDoService):
    """Handles the logic for deleting a project."""
    project_id = get_int_input("Enter project ID to delete: ")
    service.delete_project(project_id)
    print(f"✅ SUCCESS: Project with ID {project_id} deleted.")

def handle_add_task(service: ToDoService):
    """Handles the logic for adding a task to a project."""
    project_id = get_int_input("Enter project ID to add task to: ")
    title = get_non_empty_input("Enter task title: ")
    description = get_non_empty_input("Enter task description: ")
    
    deadline_str = input("Deadline (YYYY-MM-DD) [optional]: ").strip()
    deadline: Optional[datetime] = None
    if deadline_str:
        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
        except ValueError:
            print("❌ ERROR: Invalid date format. Please use YYYY-MM-DD.")
            return

    task = service.add_task_to_project(project_id, title, description, deadline)
    print(f"✅ SUCCESS: Task '{task.title}' added to project ID {project_id}.")

def handle_edit_task(service: ToDoService):
    """Handles the logic for editing a task."""
    task_id = get_int_input("Enter task ID to edit: ")
    new_title = input("New title (leave blank to keep): ").strip()
    new_desc = input("New description (leave blank to keep): ").strip()
    new_status = input("New status (todo/doing/done) [blank to keep]: ").strip()
    new_deadline_str = input("New deadline (YYYY-MM-DD) [blank to keep]: ").strip()

    if not any([new_title, new_desc, new_status, new_deadline_str]):
        print("💡 INFO: No changes were made.")
        return

    if new_status and new_status not in ['todo', 'doing', 'done']:
        print("❌ ERROR: Invalid status. Must be 'todo', 'doing', or 'done'.")
        return

    t_deadline: Optional[datetime] = None
    if new_deadline_str:
        try:
            t_deadline = datetime.strptime(new_deadline_str, "%Y-%m-%d")
        except ValueError:
            print("❌ ERROR: Invalid date format. Please use YYYY-MM-DD.")
            return

    task = service.edit_task(
        task_id,
        new_title=new_title or None,
        new_description=new_desc or None,
        new_status=new_status or None,
        new_deadline=t_deadline
    )
    print(f"✅ SUCCESS: Task {task.id} updated.")

def handle_delete_task(service: ToDoService):
    """Handles the logic for deleting a task."""
    task_id = get_int_input("Enter task ID to delete: ")
    service.delete_task(task_id)
    print(f"✅ SUCCESS: Task with ID {task_id} deleted.")

def handle_list_tasks(service: ToDoService):
    """Handles the logic for listing tasks for a project."""
    project_id = get_int_input("Enter project ID to list tasks for: ")
    
    try:
        project = next(p for p in service.get_all_projects() if p.id == project_id)
        if not project.tasks:
            print(f"No tasks found for project '{project.name}'.")
        else:
            print(f"\n--- Tasks for Project: {project.name} ---")
            for task in project.tasks:
                deadline_info = task.deadline.strftime('%Y-%m-%d') if task.deadline else "No deadline"
                print(f"- ID: {task.id}, Title: {task.title}, Status: {task.status}, Deadline: {deadline_info}")
    except StopIteration:
        print(f"❌ ERROR: Project with ID {project_id} not found.")


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
        max_projects = int(os.getenv("MAX_PROJECTS", 10))
        max_tasks = int(os.getenv("MAX_TASKS_PER_PROJECT", 20))
    except (ValueError, TypeError):
        print("⚠️ Warning: Invalid .env config. Using default values (10 projects, 20 tasks).")
        max_projects = 10
        max_tasks = 20

    service = ToDoService(max_projects=max_projects, max_tasks_per_project=max_tasks)
    print(f"Service initialized. Max projects: {max_projects}, Max tasks per project: {max_tasks}")

    # A dictionary to map user choices to handler functions
    menu_actions = {
        '1': handle_create_project,
        '2': handle_list_projects,
        '3': handle_edit_project,
        '4': handle_delete_project,
        '5': handle_add_task,
        '6': handle_edit_task,
        '7': handle_delete_task,
        '8': handle_list_tasks,
    }

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == '0':
            print("Exiting application. Goodbye!")
            break
        
        action = menu_actions.get(choice)
        if action:
            try:
                action(service)
            except ToDoListError as e:
                print(f"❌ ERROR: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
        else:
            print("❌ ERROR: Invalid choice. Please try again.")

if __name__ == "__main__":
    main()