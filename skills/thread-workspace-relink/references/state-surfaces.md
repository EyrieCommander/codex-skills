# State Surfaces For Workspace Relink

Primary surfaces:
- `~/.codex/sessions/**/*.jsonl` and `~/.codex/archived_sessions/**/*.jsonl`
  - migrate structured `"cwd"` fields only
- `~/.codex/state_*.sqlite`
  - migrate `threads.cwd` for startup/sidebar grouping

Optional surface:
- `~/.codex/.codex-global-state.json`
  - may include old path in active workspace arrays/history
  - cosmetic + startup-workspace preference impact

Verification targets:
- Old/new counts in JSONL `cwd`
- Old/new counts in SQLite `threads.cwd`
- Spot-check selected thread IDs in `threads` table
