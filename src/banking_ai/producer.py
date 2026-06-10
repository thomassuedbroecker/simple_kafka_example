"""Kafka producer for fake banking transactions."""

import json

from confluent_kafka import Producer

from banking_ai.config import kafka_base_config, load_settings
from banking_ai.models import BankingTransaction


DEMO_TRANSACTIONS = [
    {
        "transaction_id": "txn-1001",
        "account_id": "acc-001",
        "amount": 249.99,
        "currency": "EUR",
        "merchant": "Online Electronics Store",
        "country": "DE",
        "timestamp": "2026-06-10T10:15:00Z",
        "transaction_type": "card_payment",
    },
    {
        "transaction_id": "txn-1002",
        "account_id": "acc-002",
        "amount": 39.5,
        "currency": "EUR",
        "merchant": "City Grocery",
        "country": "NL",
        "timestamp": "2026-06-10T10:20:00Z",
        "transaction_type": "card_payment",
    },
    {
        "transaction_id": "txn-1003",
        "account_id": "acc-003",
        "amount": 1499.0,
        "currency": "EUR",
        "merchant": "Luxury Watches",
        "country": "DE",
        "timestamp": "2026-06-10T10:25:00Z",
        "transaction_type": "card_payment",
    },
    {
        "transaction_id": "txn-1004",
        "account_id": "acc-004",
        "amount": 89.0,
        "currency": "EUR",
        "merchant": "Unknown Online Vendor",
        "country": "FR",
        "timestamp": "2026-06-10T10:30:00Z",
        "transaction_type": "card_payment",
    },
    {
        "transaction_id": "txn-1005",
        "account_id": "acc-005",
        "amount": 650.0,
        "currency": "EUR",
        "merchant": "Main Station ATM",
        "country": "AT",
        "timestamp": "2026-06-10T10:35:00Z",
        "transaction_type": "cash_withdrawal",
    },
    {
        "transaction_id": "txn-1006",
        "account_id": "acc-006",
        "amount": 120.0,
        "currency": "EUR",
        "merchant": "Hotel Booking",
        "country": "US",
        "timestamp": "2026-06-10T10:40:00Z",
        "transaction_type": "card_payment",
    },
    {
        "transaction_id": "txn-1007",
        "account_id": "acc-007",
        "amount": 15.75,
        "currency": "EUR",
        "merchant": "Local Bakery",
        "country": "DE",
        "timestamp": "2026-06-10T10:45:00Z",
        "transaction_type": "card_payment",
    },
    {
        "transaction_id": "txn-1008",
        "account_id": "acc-008",
        "amount": 320.0,
        "currency": "EUR",
        "merchant": "Crypto Exchange",
        "country": "DE",
        "timestamp": "2026-06-10T10:50:00Z",
        "transaction_type": "bank_transfer",
    },
    {
        "transaction_id": "txn-1009",
        "account_id": "acc-009",
        "amount": 48.25,
        "currency": "EUR",
        "merchant": "Train Tickets",
        "country": "FR",
        "timestamp": "2026-06-10T10:55:00Z",
        "transaction_type": "card_payment",
    },
    {
        "transaction_id": "txn-1010",
        "account_id": "acc-010",
        "amount": 2100.0,
        "currency": "EUR",
        "merchant": "Casino Resort",
        "country": "CH",
        "timestamp": "2026-06-10T11:00:00Z",
        "transaction_type": "card_payment",
    },
]


def delivery_report(error, message) -> None:
    if error is not None:
        print(f"Delivery failed: {error}")
        return
    print(
        "Sent "
        f"key={message.key().decode('utf-8')} "
        f"topic={message.topic()} "
        f"partition={message.partition()} "
        f"offset={message.offset()}"
    )


def main() -> None:
    settings = load_settings()
    producer = Producer(kafka_base_config(settings))

    for item in DEMO_TRANSACTIONS:
        transaction = BankingTransaction.model_validate(item)
        value = transaction.model_dump_json()
        key = transaction.transaction_id

        producer.produce(
            topic=settings.transaction_topic,
            key=key.encode("utf-8"),
            value=value.encode("utf-8"),
            callback=delivery_report,
        )
        producer.poll(0)
        print(f"Queued transaction {transaction.transaction_id}: {json.loads(value)}")

    producer.flush()
    print(f"Produced {len(DEMO_TRANSACTIONS)} demo transactions.")


if __name__ == "__main__":
    main()
