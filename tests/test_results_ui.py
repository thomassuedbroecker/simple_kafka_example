import json

import pytest

from banking_ai.results_ui import (
    _demo_topic_events,
    _find_transaction,
    _kafka_event_from_message,
    _topic_event,
)


class _FakeMessage:
    """Minimal stand-in for a confluent_kafka Message (no broker needed)."""

    def __init__(self, topic, partition, offset, key, value) -> None:
        self._topic = topic
        self._partition = partition
        self._offset = offset
        self._key = key
        self._value = value

    def topic(self):
        return self._topic

    def partition(self):
        return self._partition

    def offset(self):
        return self._offset

    def key(self):
        return self._key

    def value(self):
        return self._value


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


def test_results_ui_builds_event_from_live_kafka_message() -> None:
    message = _FakeMessage(
        topic="banking.transactions",
        partition=0,
        offset=7,
        key=b"txn-1008",
        value=json.dumps({"transaction_id": "txn-1008", "merchant": "Crypto Exchange"}).encode("utf-8"),
    )

    event = _kafka_event_from_message(message, "banking-ai-inspector")

    assert event["topic"] == "banking.transactions"
    assert event["group"] == "banking-ai-inspector"
    assert event["partition"] == 0
    assert event["offset"] == 7
    assert event["key"] == "txn-1008"
    assert event["value"]["merchant"] == "Crypto Exchange"
