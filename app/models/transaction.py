from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass
class Transaction:
    id: int
    type: str
    amount: Decimal
    category: str
    description: str
    date: date