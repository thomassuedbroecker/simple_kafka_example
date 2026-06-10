"""Kafka consumer that inspects transactions with rules, LangGraph, and Ollama."""

import argparse
import json
import sys
import time

from confluent_kafka import Consumer, KafkaException
from pydantic import ValidationError

from banking_ai.config import kafka_base_config, load_settings
from banking_ai.graph import inspect_with_graph
from banking_ai.models import BankingTransaction
from banking_ai.ollama_client import OllamaClient, OllamaError


def print_findings(transaction: BankingTransaction, findings) -> None:
    print(f"\nReceived transaction: {transaction.transaction_id}")
    print("\nRule findings:")
    if findings:
        for finding in findings:
            print(f"- {finding.rule_id}")
    else:
        print("- none")
    print("\nAI inspection:")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Consume Kafka transactions and inspect them with local Ollama."
    )
    parser.add_argument(
        "--max-messages",
        type=int,
        default=None,
        help="Stop after this many successfully inspected messages.",
    )
    parser.add_argument(
        "--idle-timeout-seconds",
        type=float,
        default=None,
        help=(
            "Stop if no Kafka messages arrive for this many seconds. "
            "Useful for demos where transactions may not have been produced yet."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    settings = load_settings()

    consumer_config = kafka_base_config(settings)
    consumer_config.update(
        {
            "group.id": settings.consumer_group_id,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": False,
        }
    )
    consumer = Consumer(consumer_config)
    ollama_client = OllamaClient(settings.ollama_base_url, settings.ollama_model)
    inspected_count = 0
    idle_started_at = time.monotonic()

    consumer.subscribe([settings.transaction_topic])
    print(
        f"Consuming from topic '{settings.transaction_topic}' "
        f"with group '{settings.consumer_group_id}'."
    )

    try:
        while args.max_messages is None or inspected_count < args.max_messages:
            message = consumer.poll(1.0)
            if message is None:
                if (
                    args.idle_timeout_seconds is not None
                    and time.monotonic() - idle_started_at >= args.idle_timeout_seconds
                ):
                    print(
                        "\nNo Kafka messages arrived within "
                        f"{args.idle_timeout_seconds:g} seconds."
                    )
                    print(
                        "Run the producer first with: "
                        "PYTHON=.venv/bin/python ./scripts/produce_demo_transactions.sh"
                    )
                    print(
                        "If you already consumed these messages, use a new "
                        "CONSUMER_GROUP_ID to replay them."
                    )
                    break
                continue
            if message.error():
                raise KafkaException(message.error())
            idle_started_at = time.monotonic()

            try:
                payload = json.loads(message.value().decode("utf-8"))
                transaction = BankingTransaction.model_validate(payload)

                def stream_to_terminal(chunk: str) -> None:
                    print(chunk, end="", flush=True)

                # The graph applies deterministic rules before this callback prints
                # the findings and before Ollama explains the result.
                from banking_ai.rules import inspect_transaction_rules

                preliminary_findings = inspect_transaction_rules(transaction)
                print_findings(transaction, preliminary_findings)

                result = inspect_with_graph(
                    transaction,
                    ollama_client=ollama_client,
                    stream_writer=stream_to_terminal,
                )

                print("\n\nFinal result:")
                print(result.status)
                print(f"Reviewer check: {result.reviewer_check}")

                consumer.commit(message=message, asynchronous=False)
                inspected_count += 1

            except (json.JSONDecodeError, ValidationError) as exc:
                print(f"Skipping invalid message at offset {message.offset()}: {exc}")
                consumer.commit(message=message, asynchronous=False)
            except OllamaError as exc:
                print(f"\nOllama error: {exc}", file=sys.stderr)
                print(
                    "The Kafka offset was not committed for this message because "
                    "inspection did not complete.",
                    file=sys.stderr,
                )
                raise SystemExit(1) from exc

    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
