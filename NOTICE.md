# Notices

This repository is MIT licensed. This file tracks upstream sources, ports, adaptations, and license notes for skills copied into this repository or listed as closely related external tools.

## Included Skills

- `find-skills`: adapted from the MIT-licensed [`vercel-labs/skills`](https://github.com/vercel-labs/skills) `find-skills` skill listed on skills.sh. Skills.sh metadata was checked on 2026-05-21 and reported 1.6M installs, Vercel Labs source, and security audit badges. The packaged copy adds local-first discovery, broader scouting encouragement, and approval-bound installation safety.
- `humanize-writing`: adapted from the MIT-licensed [`blader/humanizer`](https://github.com/blader/humanizer) Claude Code skill. Upstream GitHub metadata was checked on 2026-05-21 and reported MIT. The packaged copy removes the private local voice prior from the original local install.
- `keep-codex-fast`: vendored from the MIT-licensed [`PrzemyslawKlys/keep-codex-fast`](https://github.com/PrzemyslawKlys/keep-codex-fast) maintained fork on 2026-06-04, with original upstream at [`vibeforge1111/keep-codex-fast`](https://github.com/vibeforge1111/keep-codex-fast). The packaged copy keeps the fork's safety improvements and adds quoted restore commands for paths with spaces, executable generated restore scripts, Python 3.9 compatibility, explicit closed spawned-child cleanup, and smoke-test coverage.
- `pdf`: copied from a local installed Codex PDF skill. The skill folder includes its own Apache-2.0 `LICENSE.txt`. It documents PDF rendering/review workflows plus dependencies on Poppler and Python PDF libraries such as `reportlab`, `pdfplumber`, and `pypdf`.
- `seppuku`: locally authored Codex app workflow skill for explicit thread self-archival. This is intentionally Codex-app-specific and private/power-user oriented. Covered by this repository's MIT license.
- `source-intake`: locally authored Codex workflow skill generalized from local source-intake work. The packaged copy removes private workspace paths and keeps platform-specific social/X readback separate from the general source-capture workflow. Covered by this repository's MIT license.
- `startup-pressure-test`: locally authored Codex workflow skill. No upstream source was found during the 2026-05-21 packaging provenance pass. Covered by this repository's MIT license.
- `storyboard-review`: locally authored Codex workflow skill. No upstream source was found during the 2026-05-21 packaging provenance pass. Actual video inspection depends on separate video tooling such as `video-perception` / `codex-video-vision`. Covered by this repository's MIT license.
- `thread-workspace-relink`: sourced from the MIT-licensed [`Adam-Bull/Codex-thread-toolkit`](https://github.com/Adam-Bull/Codex-thread-toolkit). Upstream GitHub metadata and license endpoint were checked on 2026-05-21 and reported MIT. The packaged copy preserves the dry-run and backup-first safety model and adds a Python 3.9 compatibility patch for local Codex environments.
- `video-perception`: adapted from the MIT-licensed [`jordanrendric/claude-video-vision`](https://github.com/jordanrendric/claude-video-vision) workflow and paired with [`EyrieCommander/codex-video-vision`](https://github.com/EyrieCommander/codex-video-vision). Included as a ready Codex app skill, but install completeness depends on the video MCP/plugin setup being present.

## Related Draft Or External Skills

- `x-skill`: local read-only X/social intake workflow developed around XMCP/X Reader work. Keep as draft until examples and source wording are sanitized.
Before public release, re-check every upstream URL, license, and copied-file boundary.
