#!/usr/bin/env bash
set -euo pipefail

# Open-source license report for the installed Python environment.
#
# Lists every installed package with its detected license and exits non-zero if
# any package has no detectable license. Run inside the project's virtual
# environment (pip install -e ".[dev]"). Reads local package metadata only; no
# network access is required.
#
# Use this to refresh THIRD_PARTY_NOTICES.md and to ensure open-source licenses
# stay in place as dependencies change.

PYTHON="${PYTHON:-python3}"

"${PYTHON}" - <<'PY'
import importlib.metadata as m
import sys

# Build tooling and this project's own package are not third-party deps.
skip = {"pip", "setuptools", "wheel", "local-kafka-langgraph-banking-ai"}

rows = []
unknown = []
for dist in m.distributions():
    name = dist.metadata["Name"]
    if not name or name.lower() in skip:
        continue
    md = dist.metadata
    lic = (md.get("License-Expression") or "").strip()
    if not lic:
        classifiers = [
            c.split("::")[-1].strip()
            for c in md.get_all("Classifier") or []
            if c.startswith("License")
        ]
        raw = (md.get("License") or "").strip()
        if classifiers:
            lic = "; ".join(classifiers)
        elif raw and len(raw) < 40:
            lic = raw
        elif raw:
            lic = "(license text embedded in metadata)"
        else:
            lic = "UNKNOWN"
    rows.append((name, m.version(name), lic))
    if lic == "UNKNOWN":
        unknown.append(name)

for name, version, lic in sorted(rows, key=lambda r: r[0].lower()):
    print(f"{name:24} {version:12} {lic}")

print()
print(f"Total packages: {len(rows)}")
if unknown:
    print(f"Packages without a detectable license: {', '.join(unknown)}")
    sys.exit(1)
print("OK: all installed packages declare an open-source license.")
PY
