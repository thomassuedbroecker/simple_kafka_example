from banking_ai.config import Settings, kafka_base_config


def test_kafka_base_config_uses_ipv4_for_local_mac_demo() -> None:
    settings = Settings(kafka_bootstrap_servers="localhost:9092")

    assert kafka_base_config(settings) == {
        "bootstrap.servers": "localhost:9092",
        "broker.address.family": "v4",
    }
