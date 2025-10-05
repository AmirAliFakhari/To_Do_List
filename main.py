# main.py

from src.todolist.services import ToDoService
from src.todolist.exceptions import ToDoListError

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
    """Main function to run the CLI application."""
    service = ToDoService(max_projects=5, max_tasks_per_project=10)

    while True:
        print_menu()
        choice = input("Enter your choice: ")

        try:
            if choice == '1':
                name = input("Enter project name: ")
                description = input("Enter project description: ")
                project = service.create_project(name, description)
                print(f"✅ SUCCESS: Project '{project.name}' created with ID {project.id}.")

            elif choice == '2':
                projects = service.get_all_projects()
                if not projects:
                    print("No projects found.")
                else:
                    print("\n--- All Projects ---")
                    for p in projects:
                        print(f"- ID: {p.id}, Name: {p.name}, Description: {p.description}, Tasks: {len(p.tasks)}")

            elif choice == '3':
                project_id = int(input("Enter the ID of the project to edit: "))
                new_name = input("Enter new name (leave blank to keep current): ")
                new_description = input("Enter new description (leave blank to keep current): ")
                
                # Use None if the input is empty
                p_name = new_name if new_name else None
                p_desc = new_description if new_description else None

                updated_project = service.edit_project(project_id, new_name=p_name, new_description=p_desc)
                print(f"✅ SUCCESS: Project {updated_project.id} updated.")

            elif choice == '4':
                project_id = int(input("Enter the ID of the project to delete: "))
                service.delete_project(project_id)
                print(f"✅ SUCCESS: Project with ID {project_id} deleted.")

            elif choice == '5':
                project_id = int(input("Enter the project ID to add the task to: "))
                title = input("Enter task title: ")
                description = input("Enter task description: ")
                task = service.add_task_to_project(project_id, title, description)
                print(f"✅ SUCCESS: Task '{task.title}' added to project ID {project_id}.")

            elif choice == '6':
                task_id = int(input("Enter the ID of the task to edit: "))
                new_title = input("Enter new title (leave blank to keep current): ")
                new_desc = input("Enter new description (leave blank to keep current): ")
                new_status = input("Enter new status (todo/doing/done) (leave blank to keep current): ")
                
                t_title = new_title if new_title else None
                t_desc = new_desc if new_desc else None
                t_status = new_status if new_status else None
                
                if t_status and t_status not in ['todo', 'doing', 'done']:
                    print("❌ ERROR: Invalid status. Must be one of 'todo', 'doing', 'done'.")
                    continue
                
                task = service.edit_task(task_id, new_title=t_title, new_description=t_desc, new_status=t_status)
                print(f"✅ SUCCESS: Task {task.id} updated.")
            
            elif choice == '7':
                task_id = int(input("Enter the ID of the task to delete: "))
                service.delete_task(task_id)
                print(f"✅ SUCCESS: Task with ID {task_id} deleted.")

            elif choice == '8':
                project_id = int(input("Enter the project ID to list tasks for: "))
                projects = service.get_all_projects()
                project = next((p for p in projects if p.id == project_id), None)
                if not project:
                    print(f"❌ ERROR: Project with ID {project_id} not found.")
                elif not project.tasks:
                    print(f"No tasks found for project '{project.name}'.")
                else:
                    print(f"\n--- Tasks for Project: {project.name} ---")
                    for t in project.tasks:
                        print(f"- ID: {t.id}, Title: {t.title}, Status: {t.status}")

            elif choice == '0':
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