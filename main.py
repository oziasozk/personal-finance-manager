from datetime import date, datetime
from decimal import Decimal, InvalidOperation

from app.models.transaction import Transaction
from app.services.finance_manager import FinanceManager
from app.database.database import create_table


create_table()

manager = FinanceManager()


def get_transaction_type():
    while True:
        transaction_type = input(
            "Type (income/expense): "
        ).strip().lower()

        if transaction_type in ["income", "expense"]:
            return transaction_type

        print("Invalid type. Please enter 'income' or 'expense'.")


def get_amount():
    while True:
        value = input("Amount: ").strip()

        try:
            amount = Decimal(value)

            if amount <= 0:
                print("Amount must be greater than 0.")
                continue

            return amount

        except InvalidOperation:
            print("Invalid amount. Please enter a valid number.")


def get_text(prompt):
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be empty.")


def get_transaction_id():
    while True:
        value = input("Transaction ID: ").strip()

        try:
            transaction_id = int(value)

            if transaction_id <= 0:
                print("ID must be greater than 0.")
                continue

            return transaction_id

        except ValueError:
            print("Invalid ID. Please enter a number.")


def get_date(prompt):
    while True:
        value = input(prompt).strip()

        try:
            return datetime.strptime(
                value,
                "%Y-%m-%d"
            ).date()

        except ValueError:
            print("Invalid date. Use YYYY-MM-DD.")
            print("Example: 2026-08-22")


def add_transaction():
    print("\n===== ADD TRANSACTION =====")

    transaction_type = get_transaction_type()
    amount = get_amount()
    category = get_text("Category: ")
    description = get_text("Description: ")

    transaction = Transaction(
        id=0,
        type=transaction_type,
        amount=amount,
        category=category,
        description=description,
        date=date.today()
    )

    manager.add_transaction(transaction)

    print("\nTransaction added successfully!")


def update_transaction():
    print("\n===== UPDATE TRANSACTION =====")

    transaction_id = get_transaction_id()
    amount = get_amount()
    category = get_text("New category: ")
    description = get_text("New description: ")

    success = manager.update_transaction(
        transaction_id,
        amount,
        category,
        description
    )

    if success:
        print("\nTransaction updated successfully!")
    else:
        print("\nTransaction not found.")


def delete_transaction():
    print("\n===== DELETE TRANSACTION =====")

    transaction_id = get_transaction_id()

    success = manager.delete_transaction(transaction_id)

    if success:
        print("\nTransaction deleted successfully!")
    else:
        print("\nTransaction not found.")


def show_financial_summary():
    total_income, total_expense, balance = (
        manager.get_financial_summary()
    )

    print("\n===== FINANCIAL SUMMARY =====")
    print(f"Total income  : {total_income:,.0f} FCFA")
    print(f"Total expense : {total_expense:,.0f} FCFA")
    print("------------------------------")
    print(f"Balance       : {balance:,.0f} FCFA")


def show_expenses_by_category():
    results = manager.get_expenses_by_category()

    print("\n===== EXPENSES BY CATEGORY =====")

    if not results:
        print("No expenses found.")
        return

    for category, total in results:
        print(f"{category:<15} : {total:,.0f} FCFA")


def show_transactions_by_date():
    print("\n===== TRANSACTIONS BY DATE =====")

    start_date = get_date(
        "Start date (YYYY-MM-DD): "
    )

    end_date = get_date(
        "End date (YYYY-MM-DD): "
    )

    if start_date > end_date:
        print("Start date cannot be after end date.")
        return

    transactions = manager.get_transactions_by_date(
        start_date,
        end_date
    )

    if not transactions:
        print("\nNo transactions found for this period.")
        return

    print("\n===== RESULTS =====")

    for transaction in transactions:
        print("\n------------------------------")
        print(f"ID          : {transaction[0]}")
        print(f"Type        : {transaction[1].upper()}")
        print(f"Amount      : {transaction[2]:,.0f} FCFA")
        print(f"Category    : {transaction[3]}")
        print(f"Description : {transaction[4]}")
        print(f"Date        : {transaction[5]}")
        print("------------------------------")


def show_dashboard():
    data = manager.get_dashboard_data()

    (
        total_income,
        total_expense,
        balance,
        income_count,
        expense_count,
        top_expense
    ) = data

    print("\n===== FINANCIAL DASHBOARD =====")

    print(
        f"Total income        : "
        f"{total_income:,.0f} FCFA"
    )

    print(
        f"Total expenses      : "
        f"{total_expense:,.0f} FCFA"
    )

    print(
        f"Current balance     : "
        f"{balance:,.0f} FCFA"
    )

    print("------------------------------")

    print(
        f"Number of incomes   : "
        f"{income_count}"
    )

    print(
        f"Number of expenses  : "
        f"{expense_count}"
    )

    print("------------------------------")

    if top_expense:
        category, amount = top_expense

        print("Top expense:")
        print(
            f"{category:<20} : "
            f"{amount:,.0f} FCFA"
        )
    else:
        print("Top expense: No expenses found.")


def main():
    while True:
        print("\n==============================")
        print("   PERSONAL FINANCE MANAGER")
        print("==============================")
        print("1. Add transaction")
        print("2. View transactions")
        print("3. Update transaction")
        print("4. Delete transaction")
        print("5. Financial summary")
        print("6. Expenses by category")
        print("7. Transactions by date")
        print("8. Financial dashboard")
        print("9. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_transaction()

        elif choice == "2":
            print("\n===== TRANSACTIONS =====")
            manager.show_transactions()

        elif choice == "3":
            update_transaction()

        elif choice == "4":
            delete_transaction()

        elif choice == "5":
            show_financial_summary()

        elif choice == "6":
            show_expenses_by_category()

        elif choice == "7":
            show_transactions_by_date()

        elif choice == "8":
            show_dashboard()

        elif choice == "9":
            print("Goodbye!")
            break

        else:
            print(
                "Invalid option. "
                "Please choose 1, 2, 3, 4, 5, 6, 7, 8 or 9."
            )


if __name__ == "__main__":
    main()