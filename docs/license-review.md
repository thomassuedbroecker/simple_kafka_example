# License Review

Date checked: 2026-06-10

Scope: repository source code, package metadata, Python dependencies installed in `.venv`, Docker Compose runtime image reference, and local Ollama/model usage notes.

This is an AI-assisted license review and not legal advice.

## Executive Summary

The repository now has an explicit MIT license for project code and package metadata. Direct Python dependencies use permissive licenses, and one transitive dependency family includes MPL-2.0 components (`certifi`, `orjson`). No strong copyleft dependency was identified from installed package metadata.

Highest-risk issue addressed: the repository previously had no project license, which made reuse and redistribution ambiguous. That is now remediated by `LICENSE`, `pyproject.toml` metadata, README links, and `THIRD_PARTY_NOTICES.md`.

## Findings

| Finding | Evidence | Impact | Status |
| --- | --- | --- | --- |
| Missing project license | No `LICENSE` file or `project.license` metadata existed before this update | External users could not clearly know reuse, modification, or redistribution rights | Fixed with MIT license |
| Missing third-party notice inventory | Dependencies were declared in `pyproject.toml`, but no notice file summarized dependency licenses | Reusers had to inspect package metadata manually | Fixed with `THIRD_PARTY_NOTICES.md` |
| Runtime model license not explicit | README referenced Ollama models, and verification used `qwen3-coder:30b`, but model files are not shipped | Users might assume model licenses are covered by the project MIT license | Fixed by documenting that model licenses must be checked separately |
| AI-assisted provenance not explicit | The repo was built through AI-assisted implementation and review, but no license/provenance note existed | Future due diligence may need review evidence and scope boundaries | Partially addressed with this review and verification docs |

## Dependency License Summary

Direct runtime dependencies:

- `confluent-kafka`: Apache Software License classifier.
- `httpx`: BSD-3-Clause.
- `langgraph`: MIT license expression.
- `pydantic`: MIT license expression.

Development dependency:

- `pytest`: MIT license expression.

Notable transitive licenses observed:

- `certifi`: MPL-2.0.
- `orjson`: MPL-2.0 AND (Apache-2.0 OR MIT).
- `typing_extensions`: PSF-2.0.
- Several dependencies use MIT, BSD, or Apache-style licenses.

See [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md) for the local inventory.

## Risk Consequence Matrix

| Risk | Legal Impact | Operational Impact | Business Impact | Security / Provenance Impact | Priority |
| --- | --- | --- | --- | --- | --- |
| Missing repository license | Ambiguous reuse and redistribution rights | Blocks clean publication or reuse | Reduces trust for open-source consumers | Weak provenance trail | P1, fixed |
| Missing third-party notices | Attribution and notice gaps during redistribution | Manual compliance work before release | Slower due diligence | Incomplete dependency transparency | P2, fixed for current dependency set |
| Model license ambiguity | Incorrect assumption that project MIT license covers model weights | Misconfigured examples if models are redistributed | Downstream compliance risk | Unclear AI artifact provenance | P2, documented |

## Repository Health Score

Current license health score: 86 / 100.

Rationale:

- Project license: 25 / 25.
- Package metadata: 20 / 20.
- Dependency transparency: 20 / 25.
- Runtime/model transparency: 12 / 15.
- Automation/SBOM maturity: 9 / 15.

Main remaining improvement: add an automated dependency license report or SBOM generation step before any formal release.

## Remediation Priority

| Priority | Action | Status |
| --- | --- | --- |
| P1 | Add repository license | Done |
| P1 | Add package license metadata | Done |
| P2 | Add third-party notices | Done |
| P2 | Document model license boundary | Done |
| P3 | Add automated SBOM or license scan command | Future improvement |
| P3 | Add contribution or DCO guidance if accepting outside contributions | Future improvement |

## Future Consequence

What is the most likely future consequence if the identified issues are not resolved within the next 12-24 months?

If licensing and notice documentation were left incomplete, the most likely consequence would be avoidable reuse friction: contributors, learners, and downstream users would hesitate to adopt or redistribute the example because project rights, dependency obligations, and model-license boundaries were unclear. Confidence: high for open-source reuse and due-diligence workflows.
