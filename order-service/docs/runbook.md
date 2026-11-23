# Order Service — Operations Runbook

## Deploy

1. Tag the release (`git tag v2.x.y`) and push.
2. CI validates the OpenAPI contract, examples, links, and diagrams.
3. The release workflow publishes the docs site and rolls out the new version.

## Rollback

If the publish produces broken docs or the deploy fails:

1. Restore the previous published artifact from the release history.
2. Revert the service to the previous tag.
3. The docs for the previous version remain available (versioned URL).

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| `GET /health` 503 | DB or event bus unreachable | Check `DATABASE_URL` / `RABBITMQ_URL`, restart dependencies |
| Orders accepted but no event | Event publish failing | Inspect `RABBITMQ_URL` + queue depth |
| Docs show stale fields | Contract changed without rebuild | Re-run the docs build pipeline |

## Escalation

`#commerce-team` on-call channel → technical owner → platform-team.
