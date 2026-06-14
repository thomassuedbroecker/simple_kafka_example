# ADR 0003: Keep Kafka scope to beginner basics

Status: Accepted

## Context

Kafka has many advanced features. Including them would make a first learning
example harder to follow.

## Decision

Teach only the core Kafka concepts: topic, producer, consumer, message key,
message value, JSON payload, consumer group, offset commit, and replay by
changing `CONSUMER_GROUP_ID`. Use a single broker, single partition, KRaft mode
(no ZooKeeper).

## Consequences

- The setup stays small and explainable.
- The following are intentionally out of scope and mentioned only as possible
  future learning topics: Schema Registry, Avro, Protobuf, Kafka transactions,
  exactly-once processing, multi-broker clusters, partition tuning, ACLs, SASL,
  TLS, Kafka Connect, and Kafka Streams.
