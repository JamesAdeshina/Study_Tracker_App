import streamlit as st
from datetime import datetime
from db import create_tables, get_courses, add_course, delete_course
from utils.course_utils import (
    log_timesheet, get_timesheets,
    add_milestone, get_milestones,
    update_milestone_status
)

st.set_page_config(page_title="Study Tracker", layout="centered")
st.title("Study Tracker App")

# Ensure database is ready
create_tables()

# --- First-Time User Experience ---
courses = get_courses()

if not courses:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135768.png", width=100)
    st.markdown("###  Welcome to Study Tracker")
    st.markdown("Let's get started by adding your first course.")

    with st.form("first_course_form"):
        name = st.text_input("Course Name")
        start = st.date_input("Start Date", datetime.today())
        weeks = st.number_input("Duration (weeks)", min_value=1)
        exam = st.date_input("Exam Date")
        submitted = st.form_submit_button("Add Course")
        if submitted and name:
            add_course(name, str(start), weeks, str(exam))
            st.success("Course added! Refresh to begin.")
            st.experimental_rerun()
    st.stop()

# --- Course Dashboard ---
st.header(" Your Courses")

for course_id, course_name in courses:
    col1, col2, col3 = st.columns([6, 1, 1])
    with col1:
        st.markdown(f"#### {course_name}")
    with col2:
        if st.button("", key=f"edit_{course_id}"):
            st.warning("Edit feature coming soon.")
    with col3:
        if st.button("", key=f"delete_{course_id}"):
            delete_course(course_id)
            st.experimental_rerun()

    if st.button("Select", key=f"select_{course_id}"):
        st.session_state.selected_course_id = course_id
        st.session_state.selected_course_name = course_name
        st.experimental_rerun()

if st.button(" Add Another Course"):
    st.session_state["show_add_form"] = True

# --- Inline Add Course ---
if st.session_state.get("show_add_form"):
    st.markdown("###  Add New Course")
    name = st.text_input("New Course Name", key="new_course_name")
    start = st.date_input("New Start Date", datetime.today(), key="new_start")
    weeks = st.number_input("New Duration (weeks)", min_value=1, key="new_duration")
    exam = st.date_input("New Exam Date", key="new_exam")
    if st.button("Create Course"):
        if name:
            add_course(name, str(start), weeks, str(exam))
            st.success("Course added!")
            st.session_state["show_add_form"] = False
            st.experimental_rerun()

# --- Course Tracker ---
if "selected_course_id" in st.session_state:
    cid = st.session_state.selected_course_id
    cname = st.session_state.selected_course_name

    st.markdown(f"##  Weekly Tracker for: **{cname}**")

    week_start = st.date_input("Week Starting", datetime.today())
    hours = st.number_input("Study Hours", min_value=0.5, step=0.5)
    topics = st.text_area("Topics Covered")
    completed = st.checkbox("Mark as Completed")

    if st.button("Save Timesheet"):
        if topics:
            log_timesheet(cid, str(week_start), hours, topics, int(completed))
            st.success("Timesheet saved.")
        else:
            st.warning("Please add some topic details.")

    rows = get_timesheets(cid)
    if rows:
        st.write(f"**Total Logged Weeks:** {len(rows)} | **Total Hours:** {sum(r[1] for r in rows):.1f}")
        st.table([{ "Week": r[0], "Hours": r[1], "Topics": r[2], "Completed": "✅" if r[3] else "❌" } for r in rows])

    # --- Milestones ---
    st.markdown("###  Milestones")
    new_ms = st.text_input("Add Milestone")
    if st.button("Save Milestone") and new_ms:
        add_milestone(cid, new_ms)
        st.success("Milestone added.")
        st.experimental_rerun()

    milestones = get_milestones(cid)
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
