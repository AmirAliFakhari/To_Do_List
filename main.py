# main.py

from datetime import datetime
from src.todolist.services import ToDoService
from src.todolist.exceptions import ToDoListError

def main():
    """Main function to run a simple test of the ToDoService."""
    service = ToDoService(max_projects=2, max_tasks_per_project=3) # Increased task limit for tests

    # --- Setup: Create projects and tasks for testing ---
    p1 = service.create_project("Personal", "Tasks for home.")
    p2 = service.create_project("Work", "Tasks for my job.")
    task1 = service.add_task_to_project(p2.id, "Finish report", "Q3 financial report.")
    task_to_delete = service.add_task_to_project(p2.id, "Delete Me", "This task will be deleted.")

    # --- New Section: Test Task Deletion ---
    print("\n--- Trying to delete a task successfully ---")
    try:
        service.delete_task(task_id=task_to_delete.id)
        print(f"✅ SUCCESS: Task '{task_to_delete.title}' (ID: {task_to_delete.id}) was deleted.")
    except ToDoListError as e:
        print(f"❌ ERROR: {e}")

    print("\n--- Trying to delete a non-existent task ---")
    try:
        service.delete_task(task_id=999)
    except ToDoListError as e:
        print(f"✅ SUCCESS: Caught expected error: {e}")


    # --- Final State Print ---
    print("\n--- Final State of Projects and Tasks ---")
    for project in service.get_all_projects():
        print(f"- Project (ID {project.id}): {project.name}")
        if project.tasks:
            for task in project.tasks:
                print(f"  - Task (ID {task.id}): {task.title} (Status: {task.status})")
        else:
            print("  (No tasks yet)")


if __name__ == "__main__":
    main()