import sqlite3
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
DATABASE = "study_tracker.db"

def create_connection():
    try:
        return sqlite3.connect(DATABASE)
    except sqlite3.Error as e:
        logging.error(f"Connection failed: {e}")
        return None

def create_tables():
    conn = create_connection()
    if not conn:
        return
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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS milestones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER,
            milestone_text TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            FOREIGN KEY(course_id) REFERENCES courses(id)
        );
    """)

    conn.commit()
    conn.close()
    logging.info("Tables created successfully.")

def get_courses():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM courses")
    courses = cursor.fetchall()
    conn.close()
    return courses

def add_course(name, start_date, duration_weeks, exam_date):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO courses (name, start_date, duration_weeks, exam_date) VALUES (?, ?, ?, ?)",
                   (name, start_date, duration_weeks, exam_date))
    conn.commit()
    conn.close()
    logging.info(f"Course added: {name}")

def delete_course(course_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM timesheets WHERE course_id = ?", (course_id,))
    cursor.execute("DELETE FROM milestones WHERE course_id = ?", (course_id,))
    cursor.execute("DELETE FROM courses WHERE id = ?", (course_id,))
    conn.commit()
    conn.close()
    logging.info(f"Course deleted: {course_id}")
