import sqlite3
from decimal import Decimal


DATABASE_NAME = "finance.db"


def get_connection(database_name=DATABASE_NAME):
    return sqlite3.connect(database_name)


def create_table(database_name=DATABASE_NAME):
    connection = get_connection(database_name)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT sql
        FROM sqlite_master
        WHERE type = 'table' AND name = 'transactions'
    """)

    table = cursor.fetchone()
    table_sql = table[0] if table else ""

    if table and "amount TEXT NOT NULL" not in table_sql:
        cursor.execute("ALTER TABLE transactions RENAME TO transactions_legacy")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            amount TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    """)

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table' AND name = 'transactions_legacy'
    """)

    if cursor.fetchone():
        cursor.execute("""
            SELECT id, type, amount, category, description, date
            FROM transactions_legacy
            ORDER BY id
        """)

        legacy_transactions = cursor.fetchall()

        cursor.executemany("""
            INSERT INTO transactions
            (id, type, amount, category, description, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, [
            (
                transaction_id,
                transaction_type,
                format(Decimal(str(amount)), "f"),
                category,
                description,
                transaction_date
            )
            for (
                transaction_id,
                transaction_type,
                amount,
                category,
                description,
                transaction_date
            ) in legacy_transactions
        ])

        cursor.execute("DROP TABLE transactions_legacy")

    connection.commit()
    connection.close()
