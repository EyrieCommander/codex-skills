# Catalog

| Skill | Status | Origin | Source URL | License | Notes |
| --- | --- | --- | --- | --- | --- |
| `find-skills` | `ready` | Vercel Labs skill adaptation | https://github.com/vercel-labs/skills | MIT | Copied with local-first discovery and approval-bound install safety changes; skills.sh metadata checked 2026-05-21. |
| `humanize-writing` | `ready` | Claude skill port/adaptation | https://github.com/blader/humanizer | MIT | Copied with private voice prior removed; upstream metadata verified 2026-05-21. |
| `startup-pressure-test` | `ready` | Local Codex skill | local authoring | MIT | Copied after privacy scan; no upstream source found during the packaging provenance pass. |
| `storyboard-review` | `ready` | Local Codex skill | local authoring | MIT | Copied after privacy scan; optional dependency on `video-perception` / `codex-video-vision` for actual video inspection. |
| `thread-workspace-relink` | `ready` | Codex skill from toolkit | https://github.com/Adam-Bull/Codex-thread-toolkit | MIT | Copied with trigger-focused description, dry-run-first workflow, backup-first apply, explicit Codex-close preference, and Python 3.9 annotation compatibility. |
| `pdf` | `ready` | Local installed Codex PDF skill | local install | Apache-2.0 | Includes PDF reading/creation/review workflow with Poppler rendering guidance and Python package dependency notes for `reportlab`, `pdfplumber`, and `pypdf`. |
| `seppuku` | `ready` | Local Codex app skill | local authoring | MIT | Codex app-specific self-archive workflow for the explicit `/seppuku` command; intentionally power-user oriented. |
| `video-perception` | `ready` | Claude video workflow adaptation plus Codex MCP/plugin | https://github.com/jordanrendric/claude-video-vision and https://github.com/EyrieCommander/codex-video-vision | MIT | Dependency-bound on the `codex-video-vision` MCP/plugin setup; included because the bundle targets Codex app installations. |
| `source-intake` | `ready` | Local Codex skill generalized from local source-intake work | local authoring | MIT | Public-neutral copy strips private project paths and keeps the X/social adapter separate; use for provenance, sensitivity, value checkpoints, entity extraction, propagation plans, and explicit reference-only/no-propagation outcomes. |
| `x-skill` | `draft` | Local workflow developed around XMCP/X Reader work | https://github.com/xdevplatform/xmcp | TBD | Formerly tracked as `x-thread-intake`; keep as X/social adapter and sanitize before publication. |
| `keep-codex-fast` | `ready` | Public Codex skill vendored from maintained fork | https://github.com/PrzemyslawKlys/keep-codex-fast | MIT | Vendored from the maintained fork after safety/privacy review; includes backup-first/report-first Codex local-state maintenance, executable restore scripts, copy-paste-safe restore commands for backup paths with spaces, Python 3.9 compatibility, explicit closed spawned-child cleanup, and smoke tests. Original upstream: https://github.com/vibeforge1111/keep-codex-fast. |

## Required Fields Before Release

Every copied skill needs:

- source URL or explicit local-authorship note;
- license/provenance classification;
- publication status;
- private-path and private-example scrub;
- safety boundary for any mutating behavior;
- install/test notes if external tools are required.

## Release Gate

Only `ready` skills are candidates for preview release. `draft`, `external_link`, and `internal_only` skills may be discussed in this catalog, but should not be presented as install-ready from this repo.
