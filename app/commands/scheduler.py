# app/commands/scheduler.py
import schedule
import time
import sys
import os
from datetime import datetime

# Add app root to path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Import the job function we just created
from app.commands.autoclose_overdue import run_autoclose

def start_scheduler():
    """
    Starts the scheduler and runs the job at the defined interval.
    """
    print(f"[{datetime.now().isoformat()}] Starting task scheduler...")
    
    # Schedule the job to run every 15 minutes
    schedule.every(15).minutes.do(run_autoclose)
    
    print(f"[{datetime.now().isoformat()}] Job 'run_autoclose' scheduled to run every 15 minutes.")
    print("Scheduler is running. Press Ctrl+C to exit.")

    # Run the scheduler loop
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            print("\nScheduler stopped manually. Goodbye!")
            break

if __name__ == "__main__":
    start_scheduler()