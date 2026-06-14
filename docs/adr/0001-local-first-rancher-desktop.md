# ADR 0001: Local-first execution with Rancher Desktop

Status: Accepted

## Context

This is a learning project for macOS Apple Silicon. Learners should be able to
run the full flow locally without cloud accounts, API keys, or paid services.

## Decision

Use **Rancher Desktop as the local container runtime** for Kafka and Kafbat UI,
driven by `docker compose`. Rancher Desktop is used only as a container runner.

## Consequences

- The project runs with `docker compose up -d` style commands.
- No cloud Kafka, no hosted services, and no API keys are required.
- Kubernetes is explicitly out of scope (see [0004](0004-no-kubernetes.md)).
- Any Docker-compatible runtime (Docker Desktop, Colima) also works, but the
  documentation standardizes on Rancher Desktop.
