# Microservices Documentation Demo

A small, **real, reproducible** example of the docs-as-code approach described in the
article *"Microservices Documentation Tools: A Practical Guide"*.

This repo proves the article's core claim by actually running it: one service, its
OpenAPI contract, its Mermaid architecture diagram, its runbook, and a CI pipeline
that validates all of them together.

## The principle

> Generate facts that already exist in code or machine-readable contracts, but keep
> operational explanations and engineering decisions under human ownership.

Each type of information has one source of truth:

| Information | Source of truth |
| --- | --- |
| HTTP API operations + schemas | `order-service/contracts/openapi.yaml` |
| Async messages | `order-service/contracts/events/order-created.json` |
| Architecture diagram | `order-service/docs/architecture.mmd` (diagrams-as-code) |
| Service purpose + ownership | `order-service/docs/index.md` (human-authored) |
| Operations/runbook | `order-service/docs/runbook.md` (human-authored) |
| Release history | `order-service/CHANGELOG.md` |

## Structure

```
order-service/
├── contracts/
│   ├── openapi.yaml          # HTTP API contract (machine-readable)
│   └── events/
│       └── order-created.json # event schema
├── docs/
│   ├── index.md              # service documentation (human-authored)
│   ├── architecture.mmd      # Mermaid diagram (source, reviewable in git)
│   └── runbook.md            # operations runbook
├── examples/
│   └── get-order-response.json # example response, validated against the schema
├── service.yaml              # service metadata (id, owner, openapi_url, version)
└── CHANGELOG.md
scripts/
├── validate-openapi.py       # structural OpenAPI + example validation
└── check-links.py            # broken internal-link check
.github/workflows/
└── documentation.yml         # CI: validate → check links → (render/build/publish hooks)
```

## Run it locally

```bash
# 1. Validate the OpenAPI contract + the example response against it
python scripts/validate-openapi.py

# 2. Check that every internal doc reference resolves
python scripts/check-links.py
```

Requires Python 3 + PyYAML (`pip install pyyaml`).

## What this demonstrates (the first-hand evidence)

1. **Contract as source of truth** — the OpenAPI spec defines the HTTP surface; the
   example response is validated against its schema, so a drift between "documented"
   and "real" is caught mechanically.
2. **Diagrams as code** — `architecture.mmd` is text in git, reviewable in a pull
   request and re-renderable in CI, not a PNG that silently rots.
3. **Generated vs human-authored boundary** — the contract, schema, and metadata can
   be generated; purpose, runbook, and design rationale are written by people.
4. **Validation in CI** — the same checks run on every pull request that touches
   contracts, docs, examples, or `service.yaml`.
