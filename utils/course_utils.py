from db import create_connection

def log_timesheet(course_id, week_start, hours, topics_covered, completed):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO timesheets (course_id, week_start, hours, topics_covered, completed) VALUES (?, ?, ?, ?, ?)",
                   (course_id, week_start, hours, topics_covered, completed))
    conn.commit()
    conn.close()

def get_timesheets(course_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT week_start, hours, topics_covered, completed FROM timesheets WHERE course_id = ?", (course_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_milestone(course_id, text):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO milestones (course_id, milestone_text, status) VALUES (?, ?, ?)",
                   (course_id, text, "pending"))
    conn.commit()
    conn.close()

def get_milestones(course_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, milestone_text, status FROM milestones WHERE course_id = ?", (course_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_milestone_status(milestone_id, status):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE milestones SET status = ? WHERE id = ?", (status, milestone_id))
    conn.commit()
    conn.close()
