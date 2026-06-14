import pytest

from banking_ai.results_ui import _find_transaction


def test_results_ui_finds_demo_transaction() -> None:
    transaction = _find_transaction("txn-1001")

    assert transaction.transaction_id == "txn-1001"
    assert transaction.merchant == "Online Electronics Store"


def test_results_ui_rejects_unknown_transaction() -> None:
    with pytest.raises(ValueError, match="Unknown transaction_id"):
        _find_transaction("missing")
