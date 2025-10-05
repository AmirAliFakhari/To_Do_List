# main.py

from datetime import datetime
from src.todolist.services import ToDoService
from src.todolist.exceptions import ToDoListError

def main():
    """Main function to run a simple test of the ToDoService."""
    service = ToDoService(max_projects=2, max_tasks_per_project=2) # Task limit را به 2 افزایش دادم

    # ... (تمام تست‌های قبلی را نگه دارید) ...
    p1 = service.create_project("Personal", "Tasks for home.")
    p2 = service.create_project("Work", "Tasks for my job.")
    task1 = service.add_task_to_project(p2.id, "Finish report", "Q3 financial report.")

    # --- بخش جدید: تست تغییر وضعیت تسک ---
    print("\n--- Trying to change task status ---")
    try:
        updated_task = service.change_task_status(task_id=task1.id, new_status="doing")
        print(f"✅ SUCCESS: Changed status of task '{updated_task.title}' to '{updated_task.status}'.")
    except ToDoListError as e:
        print(f"❌ ERROR: {e}")
        
    print("\n--- Trying to change status of a non-existent task ---")
    try:
        service.change_task_status(task_id=999, new_status="done")
    except ToDoListError as e:
        print(f"✅ SUCCESS: Caught expected error: {e}")


    # --- نمایش وضعیت نهایی ---
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