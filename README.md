# Codex Skills

Portable Codex skills and workflow patterns maintained by EyrieCommander.

This repo is a staging catalog, not a dumping ground. Skills should enter here only with clear provenance, license notes, portability status, and safety boundaries.

## Status Model

- `release_ready`: ready to publish after final review.
- `staged`: copied into this repo and scrubbed, but still waiting on repo-wide release review.
- `draft`: useful, but still needs dogfooding, dependency notes, or sanitization.
- `external_link`: maintained elsewhere; link, fork, or vendor intentionally.
- `internal_only`: too specific to a private project or local operating system to publish as-is.

## Current Direction

The first candidate set is intentionally small and provenance-first:

- `humanize-writing`
- `startup-pressure-test`
- `storyboard-review`
- `thread-workspace-relink`

Other skills may be listed in the catalog before they are copied into `skills/`, but they should not be treated as release-ready until their row in `CATALOG.md` says so.

## Safety

Do not include private workspace names, local paths, connector-derived material, client or employer details, repo internals, or user-specific examples in public artifacts unless they have been sanitized.

Skills that mutate local Codex state, repo state, browser state, GitHub, email, or connector-backed data must default to report-only or approval-bound workflows.
