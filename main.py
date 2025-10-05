# main.py

from datetime import datetime
from src.todolist.services import ToDoService
from src.todolist.exceptions import ToDoListError

def main():
    # تعیین محدودیت‌های پایین برای تست
    service = ToDoService(max_projects=2, max_tasks_per_project=1)

    # --- تست‌های ساخت پروژه ---
    print("--- Trying to create valid projects ---")
    try:
        p1 = service.create_project("Personal", "Tasks for home.")
        print(f"✅ SUCCESS: Created project '{p1.name}'")
        p2 = service.create_project("Work", "Tasks for my job.")
        print(f"✅ SUCCESS: Created project '{p2.name}'")
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

    # --- تست‌های افزودن تسک ---
    print("\n--- Trying to add a valid task ---")
    try:
        task1 = service.add_task_to_project(
            project_name="Work",
            task_title="Finish report",
            task_description="Complete the Q3 financial report.",
            deadline=datetime(2025, 10, 15)
        )
        print(f"✅ SUCCESS: Added task '{task1.title}' to project 'Work'.")
    except ToDoListError as e:
        print(f"❌ ERROR: {e}")

    print("\n--- Trying to exceed the task limit ---")
    try:
        service.add_task_to_project(
            project_name="Work",
            task_title="Plan meeting",
            task_description="This should fail."
        )
    except ToDoListError as e:
        print(f"✅ SUCCESS: Caught expected error: {e}")

    print("\n--- Trying to add a task to a non-existent project ---")
    try:
        service.add_task_to_project(
            project_name="Studies",
            task_title="Read chapter 5",
            task_description="This should also fail."
        )
    except ToDoListError as e:
        print(f"✅ SUCCESS: Caught expected error: {e}")

    # --- نمایش وضعیت نهایی ---
    print("\n--- Current Projects and Tasks ---")
    for project in service.get_all_projects():
        print(f"- Project: {project.name}")
        if project.tasks:
            for task in project.tasks:
                print(f"  - Task: {task.title} (Status: {task.status})")
        else:
            print("  (No tasks yet)")


if __name__ == "__main__":
    main()