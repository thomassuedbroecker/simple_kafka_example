# Third-Party Notices

This project is MIT licensed. It also depends on third-party open-source packages and local runtime components.

This file is a transparency aid, not a replacement for the upstream license texts. For redistribution, review each upstream package and container image license in the exact versions you ship.

## Direct Runtime Dependencies

| Component | Version checked | License evidence from installed metadata | Purpose |
| --- | --- | --- | --- |
| `confluent-kafka` | 2.14.2 | Apache Software License classifier | Kafka producer, consumer, and admin client |
| `httpx` | 0.28.1 | BSD-3-Clause | Local Ollama HTTP streaming client |
| `langgraph` | 1.2.4 | MIT license expression | StateGraph inspection workflow |
| `pydantic` | 2.13.4 | MIT license expression | Typed data models |

## Development Dependency

| Component | Version checked | License evidence from installed metadata | Purpose |
| --- | --- | --- | --- |
| `pytest` | 9.0.3 | MIT license expression | Unit tests |

## Transitive Python Dependencies Observed In Local Verification

| Component | Version checked | License evidence from installed metadata |
| --- | --- | --- |
| `annotated-types` | 0.7.0 | MIT classifier |
| `anyio` | 4.13.0 | MIT license expression |
| `certifi` | 2026.5.20 | MPL-2.0 |
| `charset-normalizer` | 3.4.7 | MIT |
| `h11` | 0.16.0 | MIT |
| `httpcore` | 1.0.9 | BSD-3-Clause |
| `idna` | 3.18 | BSD-3-Clause |
| `iniconfig` | 2.3.0 | MIT |
| `jsonpatch` | 1.33 | Modified BSD License |
| `jsonpointer` | 3.1.1 | Modified BSD License |
| `langchain-core` | 1.4.3 | MIT |
| `langchain-protocol` | 0.0.16 | MIT |
| `langgraph-checkpoint` | 4.1.1 | MIT |
| `langgraph-prebuilt` | 1.1.0 | MIT |
| `langgraph-sdk` | 0.4.2 | MIT |
| `langsmith` | 0.8.11 | MIT |
| `orjson` | 3.11.9 | MPL-2.0 AND (Apache-2.0 OR MIT) |
| `ormsgpack` | 1.12.2 | Apache-2.0 OR MIT |
| `packaging` | 26.2 | Apache-2.0 OR BSD-2-Clause |
| `pluggy` | 1.6.0 | MIT |
| `pydantic_core` | 2.46.4 | MIT |
| `Pygments` | 2.20.0 | BSD-2-Clause |
| `PyYAML` | 6.0.3 | MIT |
| `requests` | 2.34.2 | Apache-2.0 |
| `requests-toolbelt` | 1.0.0 | Apache 2.0 |
| `tenacity` | 9.1.4 | Apache 2.0 |
| `typing-inspection` | 0.4.2 | MIT |
| `typing_extensions` | 4.15.0 | PSF-2.0 |
| `urllib3` | 2.7.0 | MIT |
| `uuid_utils` | 0.16.0 | BSD-3-Clause |
| `websockets` | 15.0.1 | BSD-3-Clause |
| `xxhash` | 3.7.0 | BSD |
| `zstandard` | 0.25.0 | BSD-3-Clause |

## Local Runtime Components

| Component | Version checked | License note | Distribution note |
| --- | --- | --- | --- |
| Apache Kafka container image `apache/kafka` | 3.8.1 | Apache Kafka is Apache-2.0 licensed | The image is pulled locally by Docker Compose and is not vendored in this repository |
| Ollama | local installation | Check the installed Ollama distribution license separately | Ollama is called locally over HTTP and is not vendored in this repository |
| Ollama models such as `llama3.2` or `qwen3-coder:30b` | user-selected local model | Model licenses vary by model | Model files are not vendored or redistributed by this repository |

## Compliance Notes

- Keep this file updated when dependencies or container images change.
- If distributing a bundled application, container image, binary, or vendored dependency tree, include the relevant upstream license texts and notices for the exact shipped artifacts.
- The local learning project does not include real banking data, third-party model weights, Kafka binaries, or vendored Python packages.
