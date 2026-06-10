# Third-Party Notices

Date checked: 2026-06-10

This project is MIT licensed. It also uses third-party packages, a local Kafka container image, Ollama, and user-selected local Ollama models.

This file is a transparency aid, not legal advice and not a replacement for upstream license texts. If you redistribute a bundled application, container image, vendored dependency tree, model file, or binary artifact, review and include the exact upstream license texts and notices for the artifacts you ship.

## Project Code

| Component | Version / Scope | License | Evidence | Bundled in this repo? | Notes |
| --- | --- | --- | --- | --- | --- |
| `local-kafka-langgraph-banking-ai` project code | Repository source | MIT | [LICENSE](LICENSE), [pyproject.toml](pyproject.toml) | Yes | Applies to this repository's original source code and documentation unless noted otherwise. |

## Direct Python Dependencies

These are declared in [pyproject.toml](pyproject.toml) and were checked from installed Python package metadata in `.venv`.

| Component | Version checked | License / SPDX-style evidence | Source / homepage from metadata | Used for | Bundled in this repo? |
| --- | --- | --- | --- | --- | --- |
| `confluent-kafka` | 2.14.2 | Apache Software License classifier, treated here as Apache-2.0-style evidence | <https://github.com/confluentinc/confluent-kafka-python> | Kafka producer, consumer, and admin client | No |
| `httpx` | 0.28.1 | BSD-3-Clause | <https://github.com/encode/httpx> | Direct local Ollama HTTP streaming client | No |
| `langgraph` | 1.2.4 | MIT license expression | <https://github.com/langchain-ai/langgraph/tree/main/libs/langgraph> | `StateGraph` inspection workflow | No |
| `pydantic` | 2.13.4 | MIT license expression | <https://github.com/pydantic/pydantic> | Typed transaction, finding, result, and graph state models | No |

## Development Dependency

| Component | Version checked | License / SPDX-style evidence | Source / homepage from metadata | Used for | Bundled in this repo? |
| --- | --- | --- | --- | --- | --- |
| `pytest` | 9.0.3 | MIT license expression | <https://github.com/pytest-dev/pytest> | Unit tests | No |

## Transitive Python Dependencies Observed Locally

These packages were present in the local verification environment because of the direct dependencies above. They are not vendored in this repository.

| Component | Version checked | License / SPDX-style evidence | Source / homepage from metadata |
| --- | --- | --- | --- |
| `annotated-types` | 0.7.0 | MIT classifier | <https://github.com/annotated-types/annotated-types> |
| `anyio` | 4.13.0 | MIT license expression | <https://github.com/agronholm/anyio> |
| `certifi` | 2026.5.20 | MPL-2.0 | <https://github.com/certifi/python-certifi> |
| `charset-normalizer` | 3.4.7 | MIT | <https://github.com/jawah/charset_normalizer> |
| `h11` | 0.16.0 | MIT | <https://github.com/python-hyper/h11> |
| `httpcore` | 1.0.9 | BSD-3-Clause | <https://github.com/encode/httpcore> |
| `idna` | 3.18 | BSD-3-Clause | <https://github.com/kjd/idna> |
| `iniconfig` | 2.3.0 | MIT license expression | <https://github.com/pytest-dev/iniconfig> |
| `jsonpatch` | 1.33 | Modified BSD License | <https://github.com/stefankoegl/python-json-patch> |
| `jsonpointer` | 3.1.1 | Modified BSD License | <https://github.com/stefankoegl/python-json-pointer> |
| `langchain-core` | 1.4.3 | MIT | <https://github.com/langchain-ai/langchain> |
| `langchain-protocol` | 0.0.16 | MIT | <https://github.com/langchain-ai/agent-protocol> |
| `langgraph-checkpoint` | 4.1.1 | MIT license expression | <https://github.com/langchain-ai/langgraph/tree/main/libs/checkpoint> |
| `langgraph-prebuilt` | 1.1.0 | MIT license expression | <https://github.com/langchain-ai/langgraph/tree/main/libs/prebuilt> |
| `langgraph-sdk` | 0.4.2 | MIT license expression | <https://github.com/langchain-ai/langgraph/tree/main/libs/sdk-py> |
| `langsmith` | 0.8.11 | MIT | <https://github.com/langchain-ai/langsmith-sdk> |
| `orjson` | 3.11.9 | MPL-2.0 AND (Apache-2.0 OR MIT) | <https://github.com/ijl/orjson> |
| `ormsgpack` | 1.12.2 | Apache-2.0 OR MIT | <https://github.com/ormsgpack/ormsgpack> |
| `packaging` | 26.2 | Apache-2.0 OR BSD-2-Clause | <https://github.com/pypa/packaging> |
| `pluggy` | 1.6.0 | MIT | package metadata did not expose a source URL in this environment |
| `pydantic_core` | 2.46.4 | MIT license expression | <https://github.com/pydantic/pydantic/tree/main/pydantic-core> |
| `Pygments` | 2.20.0 | BSD-2-Clause | <https://github.com/pygments/pygments> |
| `PyYAML` | 6.0.3 | MIT | <https://github.com/yaml/pyyaml> |
| `requests` | 2.34.2 | Apache-2.0 | <https://github.com/psf/requests> |
| `requests-toolbelt` | 1.0.0 | Apache 2.0 | <https://github.com/requests/toolbelt> |
| `tenacity` | 9.1.4 | Apache 2.0 | <https://github.com/jd/tenacity> |
| `typing-inspection` | 0.4.2 | MIT license expression | <https://github.com/pydantic/typing-inspection> |
| `typing_extensions` | 4.15.0 | PSF-2.0 | <https://github.com/python/typing_extensions> |
| `urllib3` | 2.7.0 | MIT license expression | <https://github.com/urllib3/urllib3> |
| `uuid_utils` | 0.16.0 | BSD-3-Clause | <https://github.com/aminalaee/uuid-utils> |
| `websockets` | 15.0.1 | BSD-3-Clause | <https://github.com/python-websockets/websockets> |
| `xxhash` | 3.7.0 | BSD | <https://github.com/ifduyue/python-xxhash> |
| `zstandard` | 0.25.0 | BSD-3-Clause | <https://github.com/indygreg/python-zstandard> |

## Local Runtime Components

These components are required to run the full demo, but they are not vendored or redistributed by this repository.

| Component | Version / Artifact checked | License evidence | Source | Used for | Bundled in this repo? |
| --- | --- | --- | --- | --- | --- |
| Apache Kafka container image `apache/kafka` | 3.8.1 from [docker-compose.yml](docker-compose.yml) | Apache Kafka upstream license is Apache-2.0 | <https://github.com/apache/kafka/blob/trunk/LICENSE>, <https://hub.docker.com/r/apache/kafka> | Local one-broker Kafka in KRaft mode | No |
| Ollama application | local installation | Upstream Ollama license is MIT | <https://github.com/ollama/ollama/blob/main/LICENSE> | Local model runtime and HTTP API on `localhost:11434` | No |

## Local Ollama Models

Model files are not included in this repository. Users choose and pull models locally with `ollama pull` or `ollama run`. Model licenses can differ from the Ollama application license and from this repository's MIT license.

| Model reference used in docs/verification | License evidence checked | Source | Repository distribution status | Notes |
| --- | --- | --- | --- | --- |
| `qwen3-coder:30b` | Ollama model page exposes an Apache License Version 2.0 license entry | <https://ollama.com/library/qwen3-coder:30b> | Not bundled | Used in local smoke verification. If you redistribute the model or outputs in another project, check the exact model card/license terms. |
| `llama3.2` | No license entry was visible in the fetched Ollama library page during this review | <https://ollama.com/library/llama3.2> | Not bundled | Default configured model name only. Users must check the model page and upstream model license before redistribution. |
| `granite4:350m-h` | Not rechecked during this license pass | local installed model used during earlier verification | Not bundled | Mentioned only as a local verification model. Check its upstream model license before redistribution. |

## Obligation Notes For This Repository

- MIT, BSD, Apache-2.0, and PSF-2.0 dependencies generally require preserving copyright and license notices when redistributing copies.
- Apache-2.0 dependencies also include patent-license and NOTICE handling terms. Preserve upstream NOTICE files if you redistribute Apache-licensed artifacts.
- MPL-2.0 dependencies such as `certifi` and the MPL portion of `orjson` are file-level copyleft licenses. This repository does not modify or vendor those files, but redistribution of bundled dependencies should preserve their MPL license texts and source availability obligations for the MPL-covered files.
- This repository does not vendor Python packages, Kafka binaries, Kafka container layers, Ollama binaries, or model weights.
- `pip install -e ".[dev]"`, `docker compose up`, and `ollama pull` download artifacts into the user's local environment. Those downloaded artifacts keep their own upstream licenses.

## How To Refresh This Inventory

1. Recreate the virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

2. Inspect installed package metadata:

```bash
.venv/bin/python -m pip list
.venv/bin/python -m pip show confluent-kafka httpx langgraph pydantic pytest
```

3. Recheck runtime artifacts:

```bash
docker compose config
ollama list
```

4. Update this file whenever [pyproject.toml](pyproject.toml), [docker-compose.yml](docker-compose.yml), or documented Ollama model names change.
