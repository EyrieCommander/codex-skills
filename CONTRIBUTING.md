# Contributing

This repository is currently a `v0.1.0-preview` staging repo. Skills enter here only with clear provenance, license notes, portability status, and safety boundaries.

## Status Model

- `ready`: copied into this repo, scrubbed, covered by provenance/license notes, and suitable for preview testing.
- `draft`: useful, but still needs dogfooding, dependency notes, examples, or sanitization.
- `external_link`: maintained elsewhere; link, fork, or vendor intentionally.
- `internal_only`: too specific to a private project or local operating system to publish as-is.

Draft or linked candidates stay in `CATALOG.md` until they pass dependency, privacy, and safety review. Do not present a draft skill as install-ready from this repo.

## Safety Rules

Do not include private workspace names, local paths, connector-derived material, client or employer details, repo internals, or user-specific examples in public artifacts unless they have been intentionally sanitized.

Skills that mutate local Codex state, repo state, browser state, GitHub, email, or connector-backed data must default to report-only, dry-run-first, backup-first, or approval-bound workflows.

## Skill Shape

```text
skills/<skill-name>/SKILL.md
skills/<skill-name>/references/
skills/<skill-name>/agents/openai.yaml
```

References and agent templates are optional. Keep each skill self-contained enough that a user can understand its trigger, workflow, dependencies, and safety boundary from the skill folder.

## Release Checklist

Before a public release:

- verify `CATALOG.md` status and provenance for every included skill;
- verify `NOTICE.md` includes third-party sources and adaptation notes;
- run a private-path and private-example scrub;
- install-test each `ready` skill from this repo into a clean Codex skills directory;
- decide whether draft skills stay catalog-only or move into a separate branch;
- tag a preview release before making the repo public.
