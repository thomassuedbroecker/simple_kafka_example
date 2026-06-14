# ADR 0004: No Kubernetes

Status: Accepted

## Context

Rancher Desktop can run Kubernetes, so a reader might assume this project uses
it. It does not.

## Decision

Kubernetes is out of scope. The project uses Rancher Desktop only as a local
container runtime through `docker compose`. Kubernetes should be disabled in
Rancher Desktop.

## Consequences

- No Kubernetes manifests, Helm charts, `kubectl` commands, or k3s / k3d / kind
  / minikube instructions are added.
- No Kubernetes deployment files or architecture explanations are added.
- The container setup stays a simple, single-machine learning environment.
