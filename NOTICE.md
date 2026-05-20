# Notices

This repository is MIT licensed. This file tracks upstream sources, ports, adaptations, and license notes for skills copied into this repository or listed as closely related external tools.

## Included Skills

- `humanize-writing`: adapted from the MIT-licensed [`blader/humanizer`](https://github.com/blader/humanizer) Claude Code skill. Upstream GitHub metadata was checked on 2026-05-21 and reported MIT. The packaged copy removes the private local voice prior from the original local install.
- `startup-pressure-test`: locally authored Codex workflow skill. No upstream source was found during the 2026-05-21 packaging provenance pass. Covered by this repository's MIT license.
- `storyboard-review`: locally authored Codex workflow skill. No upstream source was found during the 2026-05-21 packaging provenance pass. Actual video inspection depends on separate video tooling such as `video-perception` / `codex-video-vision`. Covered by this repository's MIT license.
- `thread-workspace-relink`: sourced from the MIT-licensed [`Adam-Bull/Codex-thread-toolkit`](https://github.com/Adam-Bull/Codex-thread-toolkit). Upstream GitHub metadata and license endpoint were checked on 2026-05-21 and reported MIT. The packaged copy preserves the dry-run and backup-first safety model and adds a Python 3.9 compatibility patch for local Codex environments.

## Related Draft Or External Skills

- `video-perception`: adapted from the MIT-licensed `jordanrendric/claude-video-vision` workflow and paired with `EyrieCommander/codex-video-vision`. Keep as draft until dependency, install, and smoke-test notes are complete.
- `source-intake`: local generalized workflow candidate. Keep as draft until at least one non-X dogfood pass proves the workflow handles both propagation and `reference_only` outcomes.
- `x-skill`: local read-only X/social intake workflow developed around XMCP/X Reader work. Keep as draft until examples and source wording are sanitized.
- `keep-codex-fast`: maintained upstream at [`vibeforge1111/keep-codex-fast`](https://github.com/vibeforge1111/keep-codex-fast). This repo should link, fork, or vendor intentionally rather than presenting it as original local work.

Before public release, re-check every upstream URL, license, and copied-file boundary.
