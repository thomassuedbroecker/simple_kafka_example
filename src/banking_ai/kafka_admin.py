"""Small Kafka topic creation helper."""

from confluent_kafka.admin import AdminClient, NewTopic

from banking_ai.config import kafka_base_config, load_settings


def create_topics() -> None:
    settings = load_settings()
    admin = AdminClient(kafka_base_config(settings))
    topic = NewTopic(settings.transaction_topic, num_partitions=1, replication_factor=1)
    futures = admin.create_topics([topic])

    for topic_name, future in futures.items():
        try:
            future.result()
            print(f"Created topic: {topic_name}")
        except Exception as exc:
            if "already exists" in str(exc).lower():
                print(f"Topic already exists: {topic_name}")
            else:
                raise


if __name__ == "__main__":
    create_topics()
