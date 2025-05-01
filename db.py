import sqlite3
import logging
from time import time

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DATABASE = "study_tracker.db"

def create_connection():
    """Establish a SQLite database connection."""
    try:
        conn = sqlite3.connect(DATABASE)
        logging.info("Connected to the SQLite database.")
        return conn
    except sqlite3.Error as e:
        logging.error(f"Connection error: {e}")
        return None

def create_courses_table(cursor):
    """Create the courses table."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            start_date TEXT NOT NULL,
            duration_weeks INTEGER NOT NULL,
            exam_date TEXT NOT NULL
        );
    """)

def create_timesheets_table(cursor):
    """Create the timesheets table."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS timesheets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER,
            week_start TEXT NOT NULL,
            hours REAL NOT NULL,
            topics_covered TEXT NOT NULL,
            completed INTEGER NOT NULL,
            FOREIGN KEY(course_id) REFERENCES courses(id)
        );
    """)

def create_milestones_table(cursor):
    """Create the milestones table."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS milestones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER,
            milestone_text TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            FOREIGN KEY(course_id) REFERENCES courses(id)
        );
    """)

def create_tables():
    """Create all required tables."""
    start = time()
    conn = create_connection()
    if not conn:
        return
    cursor = conn.cursor()

    try:
        create_courses_table(cursor)
        create_timesheets_table(cursor)
        create_milestones_table(cursor)

        conn.commit()
        logging.info("All tables created successfully.")
    except sqlite3.Error as e:
        logging.error(f"Error during table creation: {e}")
    finally:
        conn.close()
        logging.info(f"Table creation completed in {time() - start:.2f} seconds.")

# Run when this file is executed directly
if __name__ == "__main__":
    create_tables()
