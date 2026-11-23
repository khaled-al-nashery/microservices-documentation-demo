# Order Service

Owned by **commerce-team**. Repository: `order-service`.

## Overview

The order service owns order creation, retrieval, and status tracking. It exposes
an HTTP API (see `contracts/openapi.yaml`) and publishes an `OrderCreated` event
(see `contracts/events/order-created.json`).

- **Purpose:** capture and track customer orders.
- **Status:** active (v2).
- **Technical owner:** commerce-team.

## Architecture

See [architecture diagram](architecture.mmd) (rendered to `architecture.svg` by CI).

Upstream services: payment-service, inventory-service (via events).
Downstream services: notification-service.

## Interfaces

- **OpenAPI specification:** `contracts/openapi.yaml`
- **Published events:** `OrderCreated`
- **Authentication:** OAuth2 bearer token (production only).
- **Compatibility policy:** additive changes only; breaking changes require a new
  major version and a consumer migration window.

## Configuration

Required environment variables (see the deployment runbook):

- `DATABASE_URL` — primary store connection string.
- `RABBITMQ_URL` — event bus connection string.
- `ORDER_QUEUE` — queue name for order events.

## Deployment

See [operations runbook](runbook.md). Deployment is a Git-tagged release; the
documentation site is rebuilt and published in the same release pipeline.

## Operations

- **Health check:** `GET /health` returns `200` when the DB and event bus are reachable.
- **Monitoring:** order-create latency + error rate (p95 < 250ms target).
- **Runbook:** see `runbook.md`.
- **Escalation:** `#commerce-team` on-call channel.

## Changelog

See `CHANGELOG.md` for release history.
