# main.py

from datetime import datetime
from src.todolist.services import ToDoService
from src.todolist.exceptions import ToDoListError

def main():
    service = ToDoService(max_projects=5, max_tasks_per_project=5)

    # --- Setup ---
    p1 = service.create_project("Personal", "Personal tasks.")
    p2 = service.create_project("Work", "Work-related tasks.")
    
    # --- Test Project Editing ---
    print("\n--- Trying to edit a project successfully ---")
    try:
        edited_p1 = service.edit_project(
            project_id=p1.id,
            new_name="Home",
            new_description="All tasks related to home."
        )
        print(f"✅ SUCCESS: Project {p1.id} name changed to '{edited_p1.name}'.")
    except ToDoListError as e:
        print(f"❌ ERROR: {e}")

    print("\n--- Trying to edit a project with a duplicate name ---")
    try:
        service.edit_project(project_id=p1.id, new_name="Work")
    except ToDoListError as e:
        print(f"✅ SUCCESS: Caught expected error: {e}")

    print("\n--- Trying to edit a project with invalid data ---")
    try:
        # Using a foolproof long string to ensure validation triggers
        long_description = "a" * 160
        service.edit_project(
            project_id=p1.id,
            new_description=long_description
        )
    except ToDoListError as e:
        print(f"✅ SUCCESS: Caught expected error: {e}")

    # --- Final State Print ---
    print("\n--- Final State of Projects ---")
    for project in service.get_all_projects():
        print(f"- Project (ID {project.id}): {project.name} - {project.description}")


if __name__ == "__main__":
    main()