import sqlite3
from pathlib import Path


DATABASE_NAME = "finance.db"


def get_connection(database_name=DATABASE_NAME):
    connection = sqlite3.connect(database_name)
    return connection


def create_table(database_name=DATABASE_NAME):
    connection = get_connection(database_name)

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