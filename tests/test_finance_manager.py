import sqlite3
from datetime import date
from decimal import Decimal

import pytest

from app.database.database import create_table
from app.models.transaction import Transaction
from app.services.finance_manager import FinanceManager


def create_transaction(
    transaction_type,
    amount,
    category,
    description
):
    return Transaction(
        id=0,
        type=transaction_type,
        amount=Decimal(str(amount)),
        category=category,
        description=description,
        date=date.today()
    )


@pytest.fixture
def test_database(tmp_path, monkeypatch):
    database_path = tmp_path / "test_finance.db"

    import app.database.database as database
    import app.services.finance_manager as finance_manager

    monkeypatch.setattr(
        database,
        "DATABASE_NAME",
        str(database_path)
    )

    monkeypatch.setattr(
        finance_manager,
        "get_connection",
        lambda: sqlite3.connect(database_path)
    )

    create_table(str(database_path))

    return database_path


def test_add_transaction(test_database):
    manager = FinanceManager()

    transaction = create_transaction(
        "expense",
        10000,
        "Food",
        "Lunch"
    )

    manager.add_transaction(transaction)

    transactions = manager.get_transactions_by_date(
        date.today(),
        date.today()
    )

    assert len(transactions) == 1
    assert transactions[0][1] == "expense"
    assert transactions[0][2] == 10000
    assert transactions[0][3] == "Food"


def test_financial_summary(test_database):
    manager = FinanceManager()

    income = create_transaction(
        "income",
        200000,
        "Salary",
        "Monthly salary"
    )

    expense = create_transaction(
        "expense",
        50000,
        "Food",
        "Groceries"
    )

    manager.add_transaction(income)
    manager.add_transaction(expense)

    total_income, total_expense, balance = (
        manager.get_financial_summary()
    )

    assert total_income == 200000
    assert total_expense == 50000
    assert balance == 150000


def test_expenses_by_category(test_database):
    manager = FinanceManager()

    expense1 = create_transaction(
        "expense",
        30000,
        "Food",
        "Groceries"
    )

    expense2 = create_transaction(
        "expense",
        10000,
        "Transport",
        "Taxi"
    )

    manager.add_transaction(expense1)
    manager.add_transaction(expense2)

    results = manager.get_expenses_by_category()

    assert results == [
        ("Food", 30000),
        ("Transport", 10000)
    ]


def test_update_transaction(test_database):
    manager = FinanceManager()

    transaction = create_transaction(
        "expense",
        5000,
        "Food",
        "Lunch"
    )

    manager.add_transaction(transaction)

    transactions = manager.get_transactions_by_date(
        date.today(),
        date.today()
    )

    transaction_id = transactions[0][0]

    success = manager.update_transaction(
        transaction_id,
        8000,
        "Transport",
        "Taxi"
    )

    assert success is True

    updated_transactions = manager.get_transactions_by_date(
        date.today(),
        date.today()
    )

    assert len(updated_transactions) == 1
    assert updated_transactions[0][2] == 8000
    assert updated_transactions[0][3] == "Transport"
    assert updated_transactions[0][4] == "Taxi"


def test_delete_transaction(test_database):
    manager = FinanceManager()

    transaction = create_transaction(
        "expense",
        7000,
        "Shopping",
        "Clothes"
    )

    manager.add_transaction(transaction)

    transactions = manager.get_transactions_by_date(
        date.today(),
        date.today()
    )

    transaction_id = transactions[0][0]

    success = manager.delete_transaction(transaction_id)

    assert success is True

    remaining_transactions = manager.get_transactions_by_date(
        date.today(),
        date.today()
    )

    assert remaining_transactions == []


def test_decimal_amounts_are_stored_and_summed_exactly(
    test_database
):
    manager = FinanceManager()

    manager.add_transaction(
        create_transaction(
            "income",
            "0.1",
            "Savings",
            "First deposit"
        )
    )

    manager.add_transaction(
        create_transaction(
            "income",
            "0.2",
            "Savings",
            "Second deposit"
        )
    )

    total_income, total_expense, balance = (
        manager.get_financial_summary()
    )

    connection = sqlite3.connect(test_database)
    stored_amount, storage_type = connection.execute("""
        SELECT amount, typeof(amount)
        FROM transactions
        WHERE description = 'First deposit'
    """).fetchone()
    connection.close()

    assert stored_amount == "0.1"
    assert storage_type == "text"
    assert total_income == Decimal("0.3")
    assert total_expense == Decimal("0")
    assert balance == Decimal("0.3")


def test_create_table_migrates_legacy_real_amounts(tmp_path):
    database_path = tmp_path / "legacy_finance.db"
    connection = sqlite3.connect(database_path)

    connection.execute("""
        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    """)

    connection.execute("""
        INSERT INTO transactions
        (type, amount, category, description, date)
        VALUES (?, ?, ?, ?, ?)
    """, (
        "income",
        1250.5,
        "Salary",
        "Legacy transaction",
        str(date.today())
    ))

    connection.commit()
    connection.close()

    create_table(str(database_path))

    connection = sqlite3.connect(database_path)
    amount, storage_type = connection.execute("""
        SELECT amount, typeof(amount)
        FROM transactions
    """).fetchone()
    connection.close()

    assert amount == "1250.5"
    assert storage_type == "text"
