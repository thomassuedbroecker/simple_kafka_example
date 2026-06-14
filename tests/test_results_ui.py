import pytest

from banking_ai.results_ui import _demo_topic_events, _find_transaction, _topic_event


def test_results_ui_finds_demo_transaction() -> None:
    transaction = _find_transaction("txn-1001")

    assert transaction.transaction_id == "txn-1001"
    assert transaction.merchant == "Online Electronics Store"


def test_results_ui_rejects_unknown_transaction() -> None:
    with pytest.raises(ValueError, match="Unknown transaction_id"):
        _find_transaction("missing")


def test_results_ui_builds_kafka_topic_event() -> None:
    transaction = _find_transaction("txn-1001")
    event = _topic_event(transaction, "banking.transactions")

    assert event["topic"] == "banking.transactions"
    assert event["key"] == "txn-1001"
    assert event["value"]["transaction_id"] == "txn-1001"
    assert event["value"]["merchant"] == "Online Electronics Store"


def test_results_ui_builds_all_demo_topic_events() -> None:
    events = _demo_topic_events("banking.transactions")

    assert len(events) == 10
    assert events[0]["topic"] == "banking.transactions"
    assert events[0]["key"] == "txn-1001"
