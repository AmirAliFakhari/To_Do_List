# main.py

from datetime import datetime
from src.todolist.services import ToDoService
from src.todolist.exceptions import ToDoListError

def main():
    """Main function to run a simple test of the ToDoService."""
    service = ToDoService(max_projects=2, max_tasks_per_project=1)

    # --- Project Creation Tests ---
    print("--- Trying to create valid projects ---")
    p1, p2 = None, None
    try:
        p1 = service.create_project("Personal", "Tasks for home.")
        print(f"✅ SUCCESS: Created project '{p1.name}' with ID {p1.id}")
        p2 = service.create_project("Work", "Tasks for my job.")
        print(f"✅ SUCCESS: Created project '{p2.name}' with ID {p2.id}")
    except ToDoListError as e:
        print(f"❌ ERROR: {e}")

    print("\n--- Trying to create a duplicate project ---")
    try:
        service.create_project("Work", "This should fail.")
    except ToDoListError as e:
        print(f"✅ SUCCESS: Caught expected error: {e}")

    print("\n--- Trying to exceed the project limit ---")
    try:
        service.create_project("University", "This should also fail.")
    except ToDoListError as e:
        print(f"✅ SUCCESS: Caught expected error: {e}")

    # --- Task Addition Tests ---
    print("\n--- Trying to add a valid task ---")
    if p2:
        try:
            task1 = service.add_task_to_project(
                project_id=p2.id,  # Use the project's ID
                task_title="Finish report",
                task_description="Complete the Q3 financial report.",
            )
            print(f"✅ SUCCESS: Added task '{task1.title}' with ID {task1.id} to project '{p2.name}'.")
        except ToDoListError as e:
            print(f"❌ ERROR: {e}")

    print("\n--- Trying to exceed the task limit ---")
    if p2:
        try:
            service.add_task_to_project(
                project_id=p2.id, # Use the project's ID
                task_title="Plan meeting",
                task_description="This should fail."
            )
        except ToDoListError as e:
            print(f"✅ SUCCESS: Caught expected error: {e}")

    print("\n--- Trying to add a task to a non-existent project ---")
    try:
        service.add_task_to_project(
            project_id=999, # Use a non-existent ID
            task_title="Read chapter 5",
            task_description="This should also fail."
        )
    except ToDoListError as e:
        print(f"✅ SUCCESS: Caught expected error: {e}")

    # --- Final State Print ---
    print("\n--- Current Projects and Tasks ---")
    for project in service.get_all_projects():
        print(f"- Project (ID {project.id}): {project.name}")
        if project.tasks:
            for task in project.tasks:
                print(f"  - Task (ID {task.id}): {task.title} (Status: {task.status})")
        else:
            print("  (No tasks yet)")


if __name__ == "__main__":
    main()