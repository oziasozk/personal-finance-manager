import sqlite3


DATABASE_NAME = "finance.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    return connection


def create_table():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()