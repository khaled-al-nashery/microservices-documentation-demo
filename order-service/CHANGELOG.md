# Changelog

All notable changes to the order service are documented here. Each entry links to
the pull request that introduced it.

## [v2.0.0] - 2026-11-20

### Added

- `GET /orders/{orderId}/status` endpoint.
- `OrderStatus` schema + `OrderCreated` event.

### Changed

- `status` enum now includes `CANCELLED`.

## [v1.0.0] - 2026-10-01

### Added

- Initial order create + list + get API (`POST /orders`, `GET /orders`, `GET /orders/{orderId}`).
