import pytest
from pydantic import ValidationError

from banking_ai.models import BankingTransaction


def test_transaction_model_accepts_valid_transaction() -> None:
    transaction = BankingTransaction.model_validate(
        {
            "transaction_id": "txn-1001",
            "account_id": "acc-001",
            "amount": 249.99,
            "currency": "EUR",
            "merchant": "Online Electronics Store",
            "country": "DE",
            "timestamp": "2026-06-10T10:15:00Z",
            "transaction_type": "card_payment",
        }
    )

    assert transaction.transaction_id == "txn-1001"
    assert transaction.currency == "EUR"


def test_transaction_model_rejects_negative_amount() -> None:
    with pytest.raises(ValidationError):
        BankingTransaction.model_validate(
            {
                "transaction_id": "txn-1001",
                "account_id": "acc-001",
                "amount": -1,
                "currency": "EUR",
                "merchant": "Online Electronics Store",
                "country": "DE",
                "timestamp": "2026-06-10T10:15:00Z",
                "transaction_type": "card_payment",
            }
        )
