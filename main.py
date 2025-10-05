# main.py

from datetime import datetime
from src.todolist.services import ToDoService
from src.todolist.exceptions import ToDoListError

def main():
    service = ToDoService(max_projects=5, max_tasks_per_project=5)

    # --- Setup ---
    p1 = service.create_project("Home", "Home tasks.")
    project_to_delete = service.create_project("Temporary", "This project will be deleted.")
    service.add_task_to_project(project_to_delete.id, "Some task", "This task will be cascade deleted.")
    
    # --- New Section: Test Project Deletion ---
    print("\n--- Trying to delete a project successfully ---")
    try:
        service.delete_project(project_id=project_to_delete.id)
        print(f"✅ SUCCESS: Project '{project_to_delete.name}' (ID: {project_to_delete.id}) and its tasks were deleted.")
    except ToDoListError as e:
        print(f"❌ ERROR: {e}")

    print("\n--- Trying to delete a non-existent project ---")
    try:
        service.delete_project(project_id=999)
    except ToDoListError as e:
        print(f"✅ SUCCESS: Caught expected error: {e}")

    # --- Final State Print ---
    print("\n--- Final State of Projects ---")
    projects = service.get_all_projects()
    if projects:
        for project in projects:
            print(f"- Project (ID {project.id}): {project.name}")
    else:
        print("No projects found.")


if __name__ == "__main__":
    main()