import sqlite3

def initialize_db():
    conn = sqlite3.connect("todo_list.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            deadline DATA,
            location TEXT,
            is_completed BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
