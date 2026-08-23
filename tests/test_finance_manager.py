from datetime import date
from decimal import Decimal

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


def test_add_transaction():
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

    assert len(transactions) >= 1


def test_financial_summary():
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

    assert total_income >= 200000
    assert total_expense >= 50000
    assert balance == total_income - total_expense


def test_expenses_by_category():
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

    categories = [category for category, amount in results]

    assert "Food" in categories
    assert "Transport" in categories


def test_update_transaction():
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

    transaction_id = transactions[-1][0]

    success = manager.update_transaction(
        transaction_id,
        8000,
        "Transport",
        "Taxi"
    )

    assert success is True


def test_delete_transaction():
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

    transaction_id = transactions[-1][0]

    success = manager.delete_transaction(
        transaction_id
    )

    assert success is True