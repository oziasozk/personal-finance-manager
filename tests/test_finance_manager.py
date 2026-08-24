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