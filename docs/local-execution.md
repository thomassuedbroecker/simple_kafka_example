# Local Execution

This project runs fully on a local macOS Apple Silicon machine. It uses
**Rancher Desktop only as the local container runtime**. Kubernetes is not used
and should be disabled in Rancher Desktop.

## 1. Install and configure Rancher Desktop

1. Install Rancher Desktop from <https://rancherdesktop.io>.
2. Open Rancher Desktop preferences.
3. **Disable Kubernetes.** This project does not use Kubernetes.
4. Select a Docker-compatible runtime (`dockerd` / moby).
5. Confirm the Docker CLI works:

   ```bash
   docker version
   docker compose version
   docker compose ps
   ```

Rancher Desktop is only the container runner here. There are no Kubernetes
manifests, Helm charts, or `kubectl` commands in this project.

## 2. Set up Python

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## 3. Start and stop Kafka

```bash
./scripts/start.sh   # start Kafka + Kafbat UI containers
./scripts/stop.sh    # stop and remove them
```

Kafka runs in a single local container in KRaft mode, so there is no ZooKeeper
container. Kafbat UI is an optional local browser at <http://localhost:8080>.

## 4. Start Ollama locally

In one terminal:

```bash
ollama serve
```

In another terminal, pull the configured model (default `qwen3-coder:30b`):

```bash
ollama pull qwen3-coder:30b
```

Verify Ollama:

```bash
ollama list
curl http://localhost:11434/api/tags
```

Larger models explain better but need more local resources. Override the model
with `OLLAMA_MODEL` if you have limited resources.

## 5. Run the learning flow

```bash
PYTHON=.venv/bin/python ./scripts/create_topics.sh
PYTHON=.venv/bin/python ./scripts/produce_demo_transactions.sh
PYTHON=.venv/bin/python MAX_MESSAGES=10 ./scripts/consume_and_inspect.sh
```

Or run the full happy-path demo in one step:

```bash
PYTHON=.venv/bin/python ./scripts/demo.sh
```

## 6. Verify the repository

```bash
PYTHON=.venv/bin/python ./scripts/verify.sh
```

This runs `python -m compileall src tests`, `python -m pytest`, and
`docker compose config`. None of these checks need Kafka, Ollama, or network
access except `docker compose config`, which only reads the Compose file.

See [troubleshooting.md](troubleshooting.md) if a step fails.
