# Troubleshooting

This is a local-first project. Most problems come from a container runtime,
Kafka, or Ollama not running yet.

## Troubleshooting matrix

| Problem | Check | Likely fix |
| --- | --- | --- |
| Docker command not found | `docker version` | Enable the Docker-compatible runtime in Rancher Desktop |
| Kafka not reachable | `docker compose ps` | Start containers with `./scripts/start.sh` |
| Kafbat UI not reachable | open `http://localhost:8080` | Check container logs: `docker compose logs kafbat-ui` |
| No messages consumed | change `CONSUMER_GROUP_ID` | Existing offsets were already committed; use a new group to replay |
| Ollama not reachable | `curl http://localhost:11434/api/tags` | Start `ollama serve` |
| Ollama model missing | `ollama list` | Run `ollama pull qwen3-coder:30b` |
| Python import error | `pip install -e ".[dev]"` | Reinstall the package into your virtual environment |
| Tests fail | `./scripts/verify.sh` | Fix syntax, Compose, or test errors reported by the script |

## Replay messages

The consumer commits offsets manually after a message is inspected. If a
consumer group already consumed and committed all messages, running it again
reads nothing. To replay from the beginning while learning, use a new group id:

```bash
export CONSUMER_GROUP_ID=banking-ai-inspector-run-2
PYTHON=.venv/bin/python MAX_MESSAGES=10 ./scripts/consume_and_inspect.sh
```

## Rancher Desktop and Kubernetes

This project uses Rancher Desktop only as the local container runtime.
Kubernetes is out of scope and should be disabled in Rancher Desktop. If
`docker` or `docker compose` is missing, enable the Docker-compatible runtime
(`dockerd` / moby) in Rancher Desktop preferences.
