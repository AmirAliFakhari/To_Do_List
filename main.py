# main.py

from datetime import datetime
from src.todolist.services import ToDoService
from src.todolist.exceptions import ToDoListError

def main():
    """Main function to run a simple test of the ToDoService."""
    service = ToDoService(max_projects=2, max_tasks_per_project=2)

    # --- Setup: Create projects and tasks for testing ---
    p1 = service.create_project("Personal", "Tasks for home.")
    p2 = service.create_project("Work", "Tasks for my job.")
    task1 = service.add_task_to_project(p2.id, "Finish report", "Q3 financial report.")
    service.change_task_status(task_id=task1.id, new_status="doing")

    # --- بخش جدید: تست ویرایش تسک ---
    print("\n--- Trying to edit a task successfully ---")
    try:
        edited_task = service.edit_task(
            task_id=task1.id,
            new_title="Finalize Q3 Report",
            new_deadline=datetime(2025, 12, 20)
        )
        print(f"✅ SUCCESS: Task '{task1.id}' title changed to '{edited_task.title}'.")
        print(f"✅ SUCCESS: Task '{task1.id}' deadline changed to '{edited_task.deadline}'.")
    except ToDoListError as e:
        print(f"❌ ERROR: {e}")

    print("\n--- Trying to edit a task with invalid data ---")
    try:
        service.edit_task(
            task_id=task1.id,
            new_title="This title is definitely way too long to be accepted by the system."
        )
    except ToDoListError as e:
        print(f"✅ SUCCESS: Caught expected error: {e}")


    # --- نمایش وضعیت نهایی ---
    print("\n--- Final State of Projects and Tasks ---")
    for project in service.get_all_projects():
        print(f"- Project (ID {project.id}): {project.name}")
        if project.tasks:
            for task in project.tasks:
                print(f"  - Task (ID {task.id}): {task.title} (Status: {task.status}, Deadline: {task.deadline})")
        else:
            print("  (No tasks yet)")


if __name__ == "__main__":
    main()