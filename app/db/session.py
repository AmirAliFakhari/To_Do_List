# app/db/session.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session



DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("No DATABASE_URL set for the application")

# Create the main engine
engine = create_engine(DATABASE_URL)

# Create a session factory. This is not a session itself,
# but a factory that will create sessions when called.
session_factory = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine, 
    class_=Session
)

def get_session() -> Session:
    """
    Utility function to get a new database session.
    """
    return session_factory()