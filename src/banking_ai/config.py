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
    ollama_model: str = "llama3.2"
    consumer_group_id: str = "banking-ai-inspector"


def load_settings() -> Settings:
    return Settings(
        kafka_bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
        transaction_topic=os.getenv("TRANSACTION_TOPIC", "banking.transactions"),
        inspection_topic=os.getenv(
            "INSPECTION_TOPIC", "banking.transaction.inspections"
        ),
        ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        ollama_model=os.getenv("OLLAMA_MODEL", "llama3.2"),
        consumer_group_id=os.getenv("CONSUMER_GROUP_ID", "banking-ai-inspector"),
    )
