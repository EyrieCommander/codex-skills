# Catalog

| Skill | Status | Origin | Source URL | License | Notes |
| --- | --- | --- | --- | --- | --- |
| `humanize-writing` | `staged` | Claude skill port/adaptation | https://github.com/blader/humanizer | MIT | Copied with private voice prior removed; upstream metadata verified 2026-05-21. |
| `startup-pressure-test` | `staged` | Local Codex skill | local authoring | TBD pending repo license | Copied after privacy scan; no upstream source found during the packaging provenance pass. |
| `storyboard-review` | `staged` | Local Codex skill | local authoring | TBD pending repo license | Copied after privacy scan; optional dependency on `video-perception` / `codex-video-vision` for actual video inspection. |
| `thread-workspace-relink` | `staged` | Codex skill from toolkit | https://github.com/Adam-Bull/Codex-thread-toolkit | MIT | Copied with trigger-focused description, dry-run-first workflow, backup-first apply, and explicit Codex-close preference. |
| `video-perception` | `draft` | Claude video workflow adaptation plus Codex MCP/plugin | https://github.com/jordanrendric/claude-video-vision and https://github.com/EyrieCommander/codex-video-vision | MIT | Dependency-bound; skill alone is not install-complete. |
| `source-intake` | `draft` | Local generalized workflow | TBD | TBD | Needs non-X dogfood pass and public-neutral examples. |
| `x-thread-intake` | `draft` | Local workflow developed around XMCP/X Reader work | https://github.com/xdevplatform/xmcp | TBD | Keep as X/social adapter; sanitize before publication. |
| `keep-codex-fast` | `external_link` | Existing public Codex skill | https://github.com/vibeforge1111/keep-codex-fast | MIT | Link-first. Fork or vendor only after safety/privacy review. |

## Required Fields Before Release

Every copied skill needs:

- source URL or explicit local-authorship note;
- license/provenance classification;
- publication status;
- private-path and private-example scrub;
- safety boundary for any mutating behavior;
- install/test notes if external tools are required.
