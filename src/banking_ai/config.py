"""Configuration with local defaults.

The project reads environment variables directly so learners can see exactly
which runtime values affect Kafka, Ollama, topics, and consumer groups.
"""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    kafka_bootstrap_servers: str = "localhost:9092"
    transaction_topic: str = "banking.transactions"
    inspection_topic: str = "banking.transaction.inspections"
    ollama_base_url: str = "http://localhost:11434"
    # Default local model. Override with OLLAMA_MODEL to use a smaller model if
    # you have limited local resources.
    ollama_model: str = "qwen3-coder:30b"
    consumer_group_id: str = "banking-ai-inspector"


def load_settings() -> Settings:
    return Settings(
        kafka_bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
        transaction_topic=os.getenv("TRANSACTION_TOPIC", "banking.transactions"),
        inspection_topic=os.getenv(
            "INSPECTION_TOPIC", "banking.transaction.inspections"
        ),
        ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        ollama_model=os.getenv("OLLAMA_MODEL", "qwen3-coder:30b"),
        consumer_group_id=os.getenv("CONSUMER_GROUP_ID", "banking-ai-inspector"),
    )


def kafka_base_config(settings: Settings) -> dict[str, str]:
    """Shared Kafka client settings for this local macOS learning project."""

    return {
        "bootstrap.servers": settings.kafka_bootstrap_servers,
        # macOS often resolves localhost to IPv6 first. The local Kafka container
        # is exposed on IPv4 localhost, so this avoids confusing ::1 retries.
        "broker.address.family": "v4",
    }
