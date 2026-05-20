---
name: thread-workspace-relink
description: Use when Codex threads need to be relinked to a new local workspace folder after a rename or move, chats appear under an old folder, show "working directory missing", or jump folders because local session/index state still points to an old cwd.
---

# Thread Workspace Relink

Use this skill to migrate Codex thread workspace paths from `old_path` to `new_path` safely and repeatably.

## Workflow

1. Confirm target and scope
- Collect `old_path` and `new_path`.
- Decide scope: `all` affected threads or selected `thread_ids`.

2. Run dry-run first
- Use script in `scripts/relink_thread_workspaces.py` with `--mode dry-run`.
- Review affected counts and files before writing.

3. Apply with backup
- Run with `--mode apply`.
- Prefer applying only after Codex is closed, because the app may be reading or writing the same local state.
- Script creates timestamped backup under `~/.codex/path_rename_backup_*`.
- Script updates:
  - Session JSONL `cwd` fields (`sessions/`, `archived_sessions/`)
  - State DB `threads.cwd` in `~/.codex/state_*.sqlite`

4. Verify
- Confirm old count is `0` for migrated scope.
- Spot-check requested thread IDs.
- If no compatible DB is discovered, run `--diagnose` and inspect `db_search_roots`, `db_candidates`, and `compatible_dbs`.

5. Refresh UI
- Quit/reopen Codex after apply so sidebar grouping refreshes.

## Commands

Dry-run all:
```bash
python3 scripts/relink_thread_workspaces.py \
  --old "/old/path" \
  --new "/new/path" \
  --mode dry-run \
  --scope all
```

Apply all:
```bash
python3 scripts/relink_thread_workspaces.py \
  --old "/old/path" \
  --new "/new/path" \
  --mode apply \
  --scope all
```

Dry-run selected thread IDs:
```bash
python3 scripts/relink_thread_workspaces.py \
  --old "/old/path" \
  --new "/new/path" \
  --mode dry-run \
  --scope ids \
  --ids "id1,id2,id3"
```

Apply selected thread IDs:
```bash
python3 scripts/relink_thread_workspaces.py \
  --old "/old/path" \
  --new "/new/path" \
  --mode apply \
  --scope ids \
  --ids "id1,id2,id3"
```

Diagnose DB discovery:
```bash
python3 scripts/relink_thread_workspaces.py \
  --old "/old/path" \
  --new "/new/path" \
  --mode dry-run \
  --scope all \
  --diagnose
```

Deep diagnostics (recommended for issue triage):
```bash
python3 scripts/relink_thread_workspaces.py \
  --old "/old/path" \
  --new "/new/path" \
  --mode dry-run \
  --scope all \
  --diagnose-deep
```

## Guardrails

- Do not bulk-rewrite arbitrary text/history; only structured `cwd` surfaces.
- Always run `dry-run` before `apply`.
- Always create backup before writes.
- Keep rollout reversible via backup restore.
- If JSONL matches exist but no compatible DB is found, `apply` exits with an error by default.
- Use `--db-path "/path/to/state_x.sqlite"` to include explicit DB files when discovery misses your active state DB.
- Use `--allow-jsonl-only` only when JSONL-only migration is intentional.

## Compatibility Note

- This skill targets current Codex local state surfaces (`sessions/*.jsonl`, `archived_sessions/*.jsonl`, `state_*.sqlite` with `threads.cwd`).
- Codex versions can change storage/schema details over time.
- Always run `dry-run` first and review counts before `apply`.
- If expected tables/fields are missing, stop and inspect local state layout before writing.
