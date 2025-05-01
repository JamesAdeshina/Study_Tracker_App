import streamlit as st
from datetime import datetime
from db import create_connection, create_tables
import sqlite3
import logging
from time import time

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Create tables on app startup
create_tables()

st.set_page_config(page_title="Study Tracker", layout="centered")
st.title("📘 Study Tracker App")

# --- Utility Functions ---

def get_courses():
    """Fetch all courses."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM courses")
    courses = cursor.fetchall()
    conn.close()
    return courses

def add_course(name, start_date, duration_weeks, exam_date):
    """Insert a new course into the database."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO courses (name, start_date, duration_weeks, exam_date)
        VALUES (?, ?, ?, ?)
    """, (name, start_date, duration_weeks, exam_date))
    conn.commit()
    conn.close()
    logging.info(f"Course added: {name}")

def log_timesheet(course_id, week_start, hours, topics_covered, completed):
    """Log a weekly study entry."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO timesheets (course_id, week_start, hours, topics_covered, completed)
        VALUES (?, ?, ?, ?, ?)
    """, (course_id, week_start, hours, topics_covered, completed))
    conn.commit()
    conn.close()
    logging.info(f"Timesheet logged for course_id: {course_id}")

def get_timesheets(course_id):
    """Fetch all timesheets for a course."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT week_start, hours, topics_covered, completed
        FROM timesheets
        WHERE course_id = ?
        ORDER BY week_start
    """, (course_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_milestone(course_id, text):
    """Add a new milestone for a course."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO milestones (course_id, milestone_text, status) VALUES (?, ?, ?)",
                   (course_id, text, "pending"))
    conn.commit()
    conn.close()
    logging.info(f"Milestone added: {text}")

def get_milestones(course_id):
    """Fetch all milestones for a course."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, milestone_text, status FROM milestones WHERE course_id = ?", (course_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_milestone_status(milestone_id, status):
    """Update the status of a milestone."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE milestones SET status = ? WHERE id = ?", (status, milestone_id))
    conn.commit()
    conn.close()
    logging.info(f"Milestone {milestone_id} updated to {status}")

# --- UI: Course Creation ---
st.header("🎓 Create a New Course")
course_name = st.text_input("Course Name")
start_date = st.date_input("Start Date", datetime.today())
duration_weeks = st.number_input("Duration (weeks)", min_value=1)
exam_date = st.date_input("Exam Date")

if st.button("Add Course"):
    if course_name:
        start = time()
        add_course(course_name, str(start_date), duration_weeks, str(exam_date))
        st.success(f"✅ Course '{course_name}' added!")
        st.toast("Course created.")
        logging.info(f"Course creation took {time() - start:.2f} seconds.")
    else:
        st.warning("Course name is required.")

# --- UI: Select Course ---
st.header("📂 Select a Course")
courses = get_courses()
if courses:
    selected = st.selectbox("Choose a course", courses, format_func=lambda x: x[1])
    selected_course_id = selected[0]
    selected_course_name = selected[1]

    # --- UI: Timesheet Logging ---
    st.subheader(f"📝 Log Weekly Study for: {selected_course_name}")
    week_start = st.date_input("Week Starting", datetime.today())
    hours = st.number_input("Study Hours", min_value=0.5, step=0.5)
    topics = st.text_area("Topics Covered")
    completed = st.checkbox("Mark as Completed")

    if st.button("Save Timesheet"):
        if topics:
            log_timesheet(selected_course_id, str(week_start), hours, topics, int(completed))
            st.success("✅ Timesheet saved.")
        else:
            st.warning("Please describe the topics covered.")

    # --- UI: Timesheet Table ---
    st.subheader(f"📊 Timesheet for {selected_course_name}")
    rows = get_timesheets(selected_course_id)
    if rows:
        total_hours = sum(row[1] for row in rows)
        st.markdown(f"**Total Weeks Logged:** {len(rows)}")
        st.markdown(f"**Total Hours Studied:** {total_hours:.1f}")
        st.table([{
            "Week Start": row[0],
            "Hours": row[1],
            "Topics": row[2],
            "Completed": "✅" if row[3] else "❌"
        } for row in rows])
    else:
        st.info("No timesheet entries yet.")

    # --- UI: Milestones ---
    st.subheader(f"🎯 Milestones for {selected_course_name}")
    new_milestone = st.text_input("Add a New Milestone")
    if st.button("Add Milestone"):
        if new_milestone:
            add_milestone(selected_course_id, new_milestone)
            st.success("Milestone added.")
        else:
            st.warning("Please enter a milestone.")

    milestones = get_milestones(selected_course_id)
    if milestones:
        for mid, text, status in milestones:
            col1, col2 = st.columns([6, 1])
            with col1:
                st.write(f"- {text}")
            with col2:
                if status == "pending":
                    if st.button("✅", key=f"done_{mid}"):
                        update_milestone_status(mid, "completed")
                        st.experimental_rerun()
                else:
                    st.markdown("✅")
    else:
        st.info("No milestones yet.")
else:
    st.warning("No courses found. Please create one first.")
