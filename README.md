# 💰 Personal Finance Manager

A simple personal finance management application built with Python and SQLite.

The application allows users to record, manage, and analyze their income and expenses directly from a command-line interface.

## 🚀 Features

- Add financial transactions
- View all transactions
- Update transactions
- Delete transactions
- Calculate total income
- Calculate total expenses
- Calculate current balance
- Group expenses by category
- Filter transactions by date
- Display a financial dashboard
- Automated tests with pytest

## 🛠️ Technologies

- Python 3
- SQLite
- SQL
- Pytest
- Git & GitHub

## 📂 Project Structure

```text
personal-finance-manager/
│
├── app/
│   ├── database/
│   │   └── database.py
│   │
│   ├── models/
│   │   └── transaction.py
│   │
│   └── services/
│       └── finance_manager.py
│
├── tests/
│   └── test_finance_manager.py
│
├── main.py
├── finance.db
└── README.md
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/personal-finance-manager.git
```

Enter the project directory:

```bash
cd personal-finance-manager
```

Install pytest:

```bash
python -m pip install pytest
```

## ▶️ Usage

Run the application:

```bash
python main.py
```

The application provides the following menu:

```text
1. Add transaction
2. View transactions
3. Update transaction
4. Delete transaction
5. Financial summary
6. Expenses by category
7. Transactions by date
8. Financial dashboard
9. Exit
```

## 🧪 Running Tests
Run the test suite with:
```bash
python -m pytest
```

## 📊 Financial Dashboard
The dashboard provides an overview of the user's finances, including:
- Total income
- Total expenses
- Current balance
- Number of incomes
- Number of expenses
- Top expense category

## 🔮 Future Improvements
- Graphical user interface
- Expense and income charts
- Monthly financial reports
- CSV export
- Budget management
- Authentication
- REST API
- Web version
- Mobile application

## 👨‍💻 Author
**Ozias**

Personal Finance Manager — Python project built as part of a software development portfolio.
