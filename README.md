# Codex Skills

A practical bundle of Codex skills for people who want their agents to get better at repeated work instead of rediscovering the same procedure every time.

This repository collects field-tested skills that make Codex more useful for long-lived project work: source capture, writing cleanup, PDF and video review, local Codex maintenance, workspace recovery, and structured idea critique.

## What's Included

| Skill | Use It When |
| --- | --- |
| `find-skills` | You want Codex to scout local and ecosystem skills before improvising or installing anything. |
| `humanize-writing` | You want prose edited to sound more natural while preserving meaning, facts, citations, and voice. |
| `keep-codex-fast` | Codex feels slow, sessions/logs/worktrees have grown, or you want safe report-first cleanup with backups and restore scripts. |
| `pdf` | You need Codex to read, create, inspect, or visually verify PDF files. |
| `seppuku` | A Codex thread should deliberately self-archive when explicitly told to retire. |
| `source-intake` | An inbound source should be captured with provenance, sensitivity, interpretation, and justified propagation. |
| `startup-pressure-test` | You want a startup idea evaluated directly for customer pain, proof, positioning, risks, and next tests. |
| `storyboard-review` | You need to compare a video render against a storyboard, script, shot list, narration plan, or production brief. |
| `thread-workspace-relink` | Codex threads point at old project paths after folders were moved or renamed. |
| `video-perception` | You want Codex to inspect or summarize video content through the Codex video-vision workflow. |

## Example Workflows

- **Clean up Codex safely:** run `keep-codex-fast` in report mode, inspect what would be archived, then apply only after backups and restore commands are generated.
- **Turn a source into project context:** use `source-intake` to capture a screenshot, article, paper, or post; separate facts from interpretation; then decide whether it belongs in a board item, project doc, skill, or reference file.
- **Review a video against intent:** use `video-perception` to inspect a render, then `storyboard-review` to compare it against the original plan.
- **Recover after reorganizing projects:** use `thread-workspace-relink` when old Codex threads still point at moved folders.
- **Improve a draft without sanding off the author:** use `humanize-writing` when the text is accurate but sounds too generic or machine-shaped.

## Install

From the repo root, install the ready bundle into your local Codex skills directory:

```sh
sh scripts/install.sh
```

The installer adds missing bundled skills automatically. If a skill already exists, it asks before replacing that one folder. Replaced skills are backed up under `~/.codex/skills/.codex-skills-backup-*`, and unrelated local skills are left alone.

Restart Codex or open a fresh session so the skill list reloads.

To install one skill instead, copy just that folder into `~/.codex/skills/`, or set a custom target with `CODEX_SKILLS_DIR=/path/to/skills sh scripts/install.sh`.

Some skills have external tool expectations. For example, `pdf` works best with Poppler and Python PDF libraries, and `video-perception` expects the Codex video-vision workflow to be available.

## Project Notes

See `CATALOG.md` for per-skill status, `NOTICE.md` for upstream sources and license notes, and `CONTRIBUTING.md` for release and safety rules.

## License

This repository is MIT licensed except where included skill folders carry their own upstream license files. See `NOTICE.md` and `CATALOG.md` for per-skill provenance.
