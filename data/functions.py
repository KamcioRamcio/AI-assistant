import sqlite3

DB_NAME = "todo_list.db"

def add_task(task, deadline=None, location=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todo (task, deadline, location) VALUES (?, ?, ?)", (task, deadline, location))
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, deadline, location, is_completed FROM todo")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def update_task(task_id, is_completed):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE todo SET is_completed = ? WHERE id = ?", (is_completed, task_id))
    conn.commit()
    conn.close()

def update_location(task_id, location):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE todo SET location = ? WHERE id = ?", (location, task_id))
    conn.commit()
    conn.close()

def update_deadline(task_id, deadline):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE todo SET deadline = ? WHERE id = ?", (deadline, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todo WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
