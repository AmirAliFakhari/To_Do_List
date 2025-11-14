# app/commands/autoclose_overdue.py
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Add app root to path to allow imports from app.*
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Load .env variables (like DATABASE_URL)
load_dotenv()

from app.db.session import get_session
from app.repositories import TaskRepository

def run_autoclose():
    """
    Entry point for the scheduled task.
    Initializes dependencies and runs the job.
    """
    print(f"[{datetime.now().isoformat()}] Running autoclose overdue tasks job...")
    
    # Setup session and repository
    session = get_session()
    task_repo = TaskRepository(session=session)
    
    try:
        # Call the repository method
        closed_count = task_repo.close_overdue_tasks()
        
        if closed_count > 0:
            print(f"Successfully closed {closed_count} overdue tasks.")
        else:
            print("No overdue tasks found to close.")
            
    except Exception as e:
        print(f"Error during autoclose job: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    # This allows the script to be run directly
    run_autoclose()