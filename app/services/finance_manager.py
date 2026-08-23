from app.models.transaction import Transaction
from app.database.database import get_connection


class FinanceManager:

    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction: Transaction):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO transactions
            (type, amount, category, description, date)
            VALUES (?, ?, ?, ?, ?)
        """, (
            transaction.type,
            float(transaction.amount),
            transaction.category,
            transaction.description,
            str(transaction.date)
        ))

        connection.commit()
        connection.close()

    def show_transactions(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, type, amount, category, description, date
            FROM transactions
            ORDER BY id
        """)

        transactions = cursor.fetchall()
        connection.close()

        if not transactions:
            print("No transactions found.")
            return

        for transaction in transactions:
            print("\n------------------------------")
            print(f"ID          : {transaction[0]}")
            print(f"Type        : {transaction[1].upper()}")
            print(f"Amount      : {transaction[2]:,.0f} FCFA")
            print(f"Category    : {transaction[3]}")
            print(f"Description : {transaction[4]}")
            print(f"Date        : {transaction[5]}")
            print("------------------------------")

    def update_transaction(
        self,
        transaction_id,
        amount,
        category,
        description
    ):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE transactions
            SET amount = ?, category = ?, description = ?
            WHERE id = ?
        """, (
            float(amount),
            category,
            description,
            transaction_id
        ))

        connection.commit()

        updated = cursor.rowcount

        connection.close()

        return updated > 0

    def delete_transaction(self, transaction_id):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM transactions
            WHERE id = ?
        """, (transaction_id,))

        connection.commit()

        deleted = cursor.rowcount

        connection.close()

        return deleted > 0

    def get_financial_summary(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                COALESCE(
                    SUM(
                        CASE
                            WHEN type = 'income'
                            THEN amount
                            ELSE 0
                        END
                    ),
                    0
                ),
                COALESCE(
                    SUM(
                        CASE
                            WHEN type = 'expense'
                            THEN amount
                            ELSE 0
                        END
                    ),
                    0
                )
            FROM transactions
        """)

        total_income, total_expense = cursor.fetchone()

        connection.close()

        balance = total_income - total_expense

        return total_income, total_expense, balance

    def get_expenses_by_category(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT category, SUM(amount)
            FROM transactions
            WHERE type = 'expense'
            GROUP BY category
            ORDER BY SUM(amount) DESC
        """)

        results = cursor.fetchall()

        connection.close()

        return results

    def get_transactions_by_date(self, start_date, end_date):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, type, amount, category, description, date
            FROM transactions
            WHERE date BETWEEN ? AND ?
            ORDER BY date ASC
        """, (start_date, end_date))

        transactions = cursor.fetchall()

        connection.close()

        return transactions

    def get_dashboard_data(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                COALESCE(
                    SUM(
                        CASE
                            WHEN type = 'income'
                            THEN amount
                            ELSE 0
                        END
                    ),
                    0
                ),
                COALESCE(
                    SUM(
                        CASE
                            WHEN type = 'expense'
                            THEN amount
                            ELSE 0
                        END
                    ),
                    0
                ),
                COUNT(
                    CASE
                        WHEN type = 'income'
                        THEN 1
                    END
                ),
                COUNT(
                    CASE
                        WHEN type = 'expense'
                        THEN 1
                    END
                )
            FROM transactions
        """)

        (
            total_income,
            total_expense,
            income_count,
            expense_count
        ) = cursor.fetchone()

        cursor.execute("""
            SELECT category, SUM(amount)
            FROM transactions
            WHERE type = 'expense'
            GROUP BY category
            ORDER BY SUM(amount) DESC
            LIMIT 1
        """)

        top_expense = cursor.fetchone()

        connection.close()

        balance = total_income - total_expense

        return (
            total_income,
            total_expense,
            balance,
            income_count,
            expense_count,
            top_expense
        )