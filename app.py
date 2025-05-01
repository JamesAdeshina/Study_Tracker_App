# app.py
import streamlit as st
from db import create_connection, create_tables
import sqlite3
from datetime import datetime

# Initialize DB
create_tables()

st.title("📘 Study Tracker App")

# --- Course Creation ---
st.header("🎓 Add a New Course")
course_name = st.text_input("Course Name")
start_date = st.date_input("Start Date")
duration = st.number_input("Duration (weeks)", min_value=1)
exam_date = st.date_input("Exam Date")

if st.button("Create Course"):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO courses (name, start_date, duration_weeks, exam_date) VALUES (?, ?, ?, ?)",
                   (course_name, str(start_date), duration, str(exam_date)))
    conn.commit()
    conn.close()
    st.success(f"✅ Course '{course_name}' created!")
