from decimal import Decimal

from app.database.database import get_connection
from app.models.transaction import Transaction


ZERO = Decimal("0")


def decimal_to_storage(amount):
    return format(Decimal(str(amount)), "f")


def decimal_from_storage(amount):
    return Decimal(str(amount))


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
            decimal_to_storage(transaction.amount),
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

        transactions = [
            (
                transaction_id,
                transaction_type,
                decimal_from_storage(amount),
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
            ) in cursor.fetchall()
        ]
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
            decimal_to_storage(amount),
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
            SELECT type, amount
            FROM transactions
        """)

        transactions = cursor.fetchall()

        connection.close()

        total_income = sum(
            (
                decimal_from_storage(amount)
                for transaction_type, amount in transactions
                if transaction_type == "income"
            ),
            ZERO
        )

        total_expense = sum(
            (
                decimal_from_storage(amount)
                for transaction_type, amount in transactions
                if transaction_type == "expense"
            ),
            ZERO
        )

        balance = total_income - total_expense

        return total_income, total_expense, balance

    def get_expenses_by_category(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT category, amount
            FROM transactions
            WHERE type = 'expense'
        """)

        expenses_by_category = {}

        for category, amount in cursor.fetchall():
            expenses_by_category[category] = (
                expenses_by_category.get(category, ZERO)
                + decimal_from_storage(amount)
            )

        connection.close()

        return sorted(
            expenses_by_category.items(),
            key=lambda expense: expense[1],
            reverse=True
        )

    def get_transactions_by_date(self, start_date, end_date):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, type, amount, category, description, date
            FROM transactions
            WHERE date BETWEEN ? AND ?
            ORDER BY date ASC
        """, (start_date, end_date))

        transactions = [
            (
                transaction_id,
                transaction_type,
                decimal_from_storage(amount),
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
            ) in cursor.fetchall()
        ]

        connection.close()

        return transactions

    def get_dashboard_data(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                COUNT(CASE WHEN type = 'income' THEN 1 END),
                COUNT(CASE WHEN type = 'expense' THEN 1 END)
            FROM transactions
        """)

        income_count, expense_count = cursor.fetchone()

        connection.close()

        total_income, total_expense, balance = (
            self.get_financial_summary()
        )

        expenses_by_category = self.get_expenses_by_category()
        top_expense = (
            expenses_by_category[0]
            if expenses_by_category
            else None
        )

        return (
            total_income,
            total_expense,
            balance,
            income_count,
            expense_count,
            top_expense
        )
