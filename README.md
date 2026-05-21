# Codex Skills

Portable Codex skills and workflow patterns maintained by EyrieCommander.

This repo is a staging catalog, not a dumping ground. Skills enter here only with clear provenance, license notes, portability status, and safety boundaries.

## Release Posture

This repository is currently a private `v0.1.0-preview` staging repo. The first goal is to make a small set of portable skills installable, documented, and provenance-clean before deciding whether to publish the repo.

Current ready set:

- `find-skills`
- `humanize-writing`
- `startup-pressure-test`
- `storyboard-review`
- `thread-workspace-relink`

Draft or linked candidates stay in the catalog until they pass dependency, privacy, and safety review.

## Ready Skills

| Skill | What This Copy Adds |
| --- | --- |
| `find-skills` | Adapted from Vercel Labs; encourages frequent skill scouting while checking local skills first and requiring approval before global installs. |
| `humanize-writing` | Adapted from `blader/humanizer`; removes the private local voice prior and keeps a generic voice-sample workflow. |
| `startup-pressure-test` | Local Codex workflow for direct startup idea pressure-testing, packaged after a privacy scan. |
| `storyboard-review` | Local Codex workflow for comparing a video render to a storyboard or script, with explicit caveats when video inspection tools are unavailable. |
| `thread-workspace-relink` | Adapted from `Adam-Bull/Codex-thread-toolkit`; keeps dry-run/backup-first behavior, adds a Codex-close preference, and patches Python 3.9 annotation compatibility. |

## Install A Skill Locally

Copy the skill folder into your Codex skills directory, then restart Codex or open a fresh session so the skill list reloads.

```sh
mkdir -p "$HOME/.codex/skills"
cp -R skills/humanize-writing "$HOME/.codex/skills/humanize-writing"
```

Replace `humanize-writing` with any skill folder in `skills/`. Do not install a draft skill into normal workflow until its catalog row says `ready` or you intentionally want to test it.

## Status Model

- `ready`: copied into this repo, scrubbed, covered by provenance/license notes, and suitable for private preview testing.
- `draft`: useful, but still needs dogfooding, dependency notes, examples, or sanitization.
- `external_link`: maintained elsewhere; link, fork, or vendor intentionally.
- `internal_only`: too specific to a private project or local operating system to publish as-is.

## Safety Rules

Do not include private workspace names, local paths, connector-derived material, client or employer details, repo internals, or user-specific examples in public artifacts unless they have been intentionally sanitized.

Skills that mutate local Codex state, repo state, browser state, GitHub, email, or connector-backed data must default to report-only, dry-run-first, or approval-bound workflows.

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
- tag a private preview before making the repo public.

## License

This repository is MIT licensed. Some skills are adapted from MIT-licensed upstream projects; see `NOTICE.md` and `CATALOG.md` for per-skill provenance.
