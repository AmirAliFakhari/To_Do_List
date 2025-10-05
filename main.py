# main.py

from todolist.services import ToDoService
from todolist.exceptions import ToDoListError

def main():
    service = ToDoService(max_projects=2) # Set a low limit for testing

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

    print("\n--- Current Projects ---")
    for project in service.get_all_projects():
        print(f"- {project.name}: {project.description}")


if __name__ == "__main__":
    main()