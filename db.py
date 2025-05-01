# db.py
import sqlite3

DATABASE = "study_tracker.db"

def create_connection():
    return sqlite3.connect(DATABASE)

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            start_date TEXT NOT NULL,
            duration_weeks INTEGER NOT NULL,
            exam_date TEXT NOT NULL
        );
    """)

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

    conn.commit()
    conn.close()



if __name__ == "__main__":
    create_tables()
