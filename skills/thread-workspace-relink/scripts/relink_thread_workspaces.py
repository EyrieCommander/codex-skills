#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Set, Tuple

try:
    import tomllib
except Exception:  # pragma: no cover - python<3.11 fallback
    tomllib = None  # type: ignore[assignment]


def eprint(msg: str) -> None:
    print(msg)


def parse_ids(raw: str) -> Set[str]:
    out: Set[str] = set()
    for part in (raw or "").split(","):
        t = part.strip()
        if t:
            out.add(t)
    return out


@dataclass
class JsonlEdit:
    path: Path
    old_hits: int
    new_hits: int


@dataclass
class DbEdit:
    path: Path
    old_count_before: int
    new_count_before: int
    old_count_after: int
    new_count_after: int


def collect_jsonl_files(codex_home: Path) -> List[Path]:
    roots = [codex_home / "sessions", codex_home / "archived_sessions"]
    files: List[Path] = []
    for root in roots:
        if root.exists():
            files.extend(sorted(root.rglob("*.jsonl")))
    return files


def file_mentions_any_id(path: Path, ids: Set[str]) -> bool:
    if not ids:
        return True
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return False
    return any(tid in text for tid in ids)


def count_cwd_hits(text: str, old: str, new: str) -> Tuple[int, int]:
    old_pat = re.compile(r'"cwd"\s*:\s*"' + re.escape(old) + r'"')
    new_pat = re.compile(r'"cwd"\s*:\s*"' + re.escape(new) + r'"')
    return len(old_pat.findall(text)), len(new_pat.findall(text))


def replace_cwd_hits(text: str, old: str, new: str) -> str:
    pat = re.compile(r'("cwd"\s*:\s*")' + re.escape(old) + r'(")')
    return pat.sub(r'\1' + new + r'\2', text)


def discover_jsonl_edits(files: Iterable[Path], old: str, new: str) -> List[JsonlEdit]:
    edits: List[JsonlEdit] = []
    for p in files:
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        old_hits, new_hits = count_cwd_hits(text, old, new)
        if old_hits > 0:
            edits.append(JsonlEdit(path=p, old_hits=old_hits, new_hits=new_hits))
    return edits


def parse_sqlite_home_from_config(codex_home: Path) -> Path | None:
    config_path = codex_home / "config.toml"
    if not config_path.exists():
        return None

    raw: str
    try:
        raw = config_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None

    sqlite_home_value: str | None = None
    if tomllib is not None:
        try:
            parsed = tomllib.loads(raw)
            maybe = parsed.get("sqlite_home")
            if isinstance(maybe, str) and maybe.strip():
                sqlite_home_value = maybe.strip()
        except Exception:
            sqlite_home_value = None

    # Fallback for environments without tomllib or malformed toml.
    if sqlite_home_value is None:
        m = re.search(r'(?m)^\s*sqlite_home\s*=\s*"([^"]+)"\s*$', raw)
        if m:
            sqlite_home_value = m.group(1).strip()

    if not sqlite_home_value:
        return None

    p = Path(os.path.expanduser(sqlite_home_value))
    if not p.is_absolute():
        p = codex_home / p
    return p.resolve()


def resolve_sqlite_home(codex_home: Path) -> Path | None:
    env_val = os.environ.get("CODEX_SQLITE_HOME", "").strip()
    if env_val:
        p = Path(os.path.expanduser(env_val))
        if not p.is_absolute():
            p = codex_home / p
        return p.resolve()
    return parse_sqlite_home_from_config(codex_home)


def find_state_dbs(search_roots: Iterable[Path]) -> List[Path]:
    seen: Set[Path] = set()
    out: List[Path] = []
    for root in search_roots:
        if not root.exists() or not root.is_dir():
            continue
        for p in root.glob("state_*.sqlite"):
            rp = p.resolve()
            if rp not in seen and rp.is_file():
                seen.add(rp)
                out.append(rp)
    return sorted(out)


def find_all_sqlite_like_dbs(search_roots: Iterable[Path]) -> List[Path]:
    seen: Set[Path] = set()
    out: List[Path] = []
    for root in search_roots:
        if not root.exists() or not root.is_dir():
            continue
        for p in root.rglob("*"):
            if not p.is_file():
                continue
            if p.suffix.lower() not in (".sqlite", ".db"):
                continue
            rp = p.resolve()
            if rp not in seen:
                seen.add(rp)
                out.append(rp)
    return sorted(out)


def db_has_threads_table(db_path: Path) -> bool:
    try:
        with sqlite3.connect(db_path) as con:
            cur = con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='threads'")
            return cur.fetchone() is not None
    except Exception:
        return False


def db_has_threads_cwd(db_path: Path) -> bool:
    try:
        with sqlite3.connect(db_path) as con:
            cur = con.execute("PRAGMA table_info('threads')")
            cols = [str(r[1]).lower() for r in cur.fetchall()]
            return "cwd" in cols
    except Exception:
        return False


def inspect_db(db_path: Path) -> dict:
    try:
        has_threads = db_has_threads_table(db_path)
        has_cwd = db_has_threads_cwd(db_path) if has_threads else False
        return {"path": str(db_path), "has_threads": has_threads, "has_threads_cwd": has_cwd}
    except Exception as e:
        return {"path": str(db_path), "error": str(e)}


def inspect_db_deep(db_path: Path) -> dict:
    report: dict = {"path": str(db_path)}
    try:
        with sqlite3.connect(db_path) as con:
            table_rows = con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
            tables = [str(r[0]) for r in table_rows]
            report["tables"] = tables
            report["has_threads"] = "threads" in tables

            tables_of_interest: dict = {}
            key_cols = {"cwd", "workspace", "path", "rollout_path", "thread_id", "id"}
            for table in tables:
                try:
                    col_rows = con.execute(f"PRAGMA table_info('{table}')").fetchall()
                    cols = [str(r[1]) for r in col_rows]
                except Exception:
                    continue
                if any(c.lower() in key_cols for c in cols):
                    tables_of_interest[table] = cols
            report["tables_of_interest"] = tables_of_interest

            if report["has_threads"]:
                thread_cols = tables_of_interest.get("threads", [])
                has_threads_cwd = any(c.lower() == "cwd" for c in thread_cols)
                report["has_threads_cwd"] = has_threads_cwd
                if has_threads_cwd:
                    try:
                        cnt = con.execute("SELECT COUNT(*) FROM threads").fetchone()
                        report["threads_count"] = int(cnt[0] if cnt else 0)
                    except Exception as e:
                        report["threads_count_error"] = str(e)

                    sample_query = None
                    if any(c.lower() == "updated_at" for c in thread_cols):
                        sample_query = "SELECT id, cwd, rollout_path FROM threads ORDER BY updated_at DESC LIMIT 5"
                    elif any(c.lower() == "updated_at_ms" for c in thread_cols):
                        sample_query = "SELECT id, cwd, rollout_path FROM threads ORDER BY updated_at_ms DESC LIMIT 5"
                    else:
                        sample_query = "SELECT id, cwd, rollout_path FROM threads LIMIT 5"
                    try:
                        sample = con.execute(sample_query).fetchall()
                        report["threads_sample"] = sample
                    except Exception as e:
                        report["threads_sample_error"] = str(e)
    except Exception as e:
        report["error"] = str(e)
    return report


def db_count_cwd(db_path: Path, cwd: str, ids: Set[str] | None = None) -> int:
    ids = ids or set()
    with sqlite3.connect(db_path) as con:
        if ids:
            sorted_ids = sorted(ids)
            placeholders = ",".join("?" for _ in sorted_ids)
            query = f"SELECT COUNT(*) FROM threads WHERE cwd=? AND id IN ({placeholders})"
            params = [cwd, *sorted_ids]
        else:
            query = "SELECT COUNT(*) FROM threads WHERE cwd=?"
            params = [cwd]
        cur = con.execute(query, params)
        row = cur.fetchone()
        return int(row[0] if row else 0)


def apply_db_update(db_path: Path, old: str, new: str, ids: Set[str] | None = None) -> DbEdit:
    ids = ids or set()
    with sqlite3.connect(db_path) as con:
        old_before = db_count_cwd(db_path, old, ids)
        new_before = db_count_cwd(db_path, new, ids)
        if ids:
            sorted_ids = sorted(ids)
            placeholders = ",".join("?" for _ in sorted_ids)
            query = f"UPDATE threads SET cwd=? WHERE cwd=? AND id IN ({placeholders})"
            params = [new, old, *sorted_ids]
        else:
            query = "UPDATE threads SET cwd=? WHERE cwd=?"
            params = [new, old]
        con.execute(query, params)
        con.commit()
        old_after = db_count_cwd(db_path, old, ids)
        new_after = db_count_cwd(db_path, new, ids)
    return DbEdit(
        path=db_path,
        old_count_before=old_before,
        new_count_before=new_before,
        old_count_after=old_after,
        new_count_after=new_after,
    )


def make_backup_dir(codex_home: Path) -> Path:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = codex_home / f"path_rename_backup_{ts}"
    backup_dir.mkdir(parents=True, exist_ok=False)
    return backup_dir


def backup_dest_for_file(src: Path, backup_dir: Path, codex_home: Path) -> Path:
    try:
        rel = src.relative_to(codex_home)
        return backup_dir / rel
    except Exception:
        # Keep external files reversible while avoiding absolute paths inside backup dir.
        parts = [p for p in src.resolve().parts if p not in ("/", "\\")]
        return backup_dir / "external" / Path(*parts)


def backup_file(src: Path, backup_dir: Path, codex_home: Path) -> Path:
    dst = backup_dest_for_file(src, backup_dir, codex_home)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return dst


def update_global_state_json(codex_home: Path, old: str, new: str, do_apply: bool, backup_dir: Path | None) -> bool:
    path = codex_home / ".codex-global-state.json"
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    if old not in text:
        return False
    if not do_apply:
        return True
    if backup_dir is not None:
        backup_file(path, backup_dir, codex_home)
    path.write_text(text.replace(old, new), encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="Relink Codex thread workspace paths after folder rename.")
    ap.add_argument("--old", required=True, help="Old absolute workspace path")
    ap.add_argument("--new", required=True, help="New absolute workspace path")
    ap.add_argument("--mode", choices=["dry-run", "apply"], default="dry-run")
    ap.add_argument("--scope", choices=["all", "ids"], default="all")
    ap.add_argument("--ids", default="", help="Comma-separated thread IDs when --scope ids")
    ap.add_argument("--codex-home", default=str(Path.home() / ".codex"))
    ap.add_argument("--db-path", action="append", default=[], help="Additional explicit SQLite DB path(s) to include")
    ap.add_argument("--diagnose", action="store_true", help="Print DB discovery diagnostics and exit")
    ap.add_argument(
        "--diagnose-deep",
        action="store_true",
        help="Print expanded DB/config diagnostics (all *.sqlite/*.db under search roots) and exit",
    )
    ap.add_argument(
        "--allow-jsonl-only",
        action="store_true",
        help="Allow apply success when JSONL updates are found but no compatible state DB is discovered",
    )
    ap.add_argument("--update-global-state", action="store_true", help="Also replace old path in .codex-global-state.json")
    args = ap.parse_args()

    old = args.old
    new = args.new
    codex_home = Path(args.codex_home).expanduser().resolve()
    do_apply = args.mode == "apply"

    if not Path(new).exists():
        eprint(f"ERROR: new path does not exist: {new}")
        return 2

    ids = parse_ids(args.ids)
    if args.scope == "ids" and not ids:
        eprint("ERROR: --scope ids requires --ids")
        return 2

    all_jsonl = collect_jsonl_files(codex_home)
    if args.scope == "ids":
        all_jsonl = [p for p in all_jsonl if file_mentions_any_id(p, ids)]

    jsonl_edits = discover_jsonl_edits(all_jsonl, old, new)

    sqlite_home = resolve_sqlite_home(codex_home)
    db_search_roots: List[Path] = [codex_home]
    if sqlite_home is not None and sqlite_home not in db_search_roots:
        db_search_roots.append(sqlite_home)

    explicit_db_paths: List[Path] = []
    for raw_path in args.db_path:
        p = Path(raw_path).expanduser().resolve()
        if p.exists() and p.is_file():
            explicit_db_paths.append(p)

    discovered_state_dbs = find_state_dbs(db_search_roots)
    seen_db: Set[Path] = set()
    db_candidates: List[Path] = []
    for p in [*discovered_state_dbs, *explicit_db_paths]:
        if p not in seen_db:
            seen_db.add(p)
            db_candidates.append(p)

    db_diagnostics = [inspect_db(p) for p in db_candidates]
    db_paths = [p for p in db_candidates if db_has_threads_table(p) and db_has_threads_cwd(p)]

    if args.diagnose_deep:
        deep_discovered = find_all_sqlite_like_dbs(db_search_roots)
        deep_seen: Set[Path] = set()
        deep_candidates: List[Path] = []
        for p in [*deep_discovered, *explicit_db_paths]:
            if p not in deep_seen:
                deep_seen.add(p)
                deep_candidates.append(p)
        deep_reports = [inspect_db_deep(p) for p in deep_candidates]
        deep_compatible = [
            r["path"]
            for r in deep_reports
            if r.get("has_threads") is True and r.get("has_threads_cwd") is True
        ]
        payload = {
            "mode": args.mode,
            "codex_home": str(codex_home),
            "config_toml_exists": (codex_home / "config.toml").exists(),
            "resolved_sqlite_home": str(sqlite_home) if sqlite_home else None,
            "env_CODEX_SQLITE_HOME": os.environ.get("CODEX_SQLITE_HOME", None),
            "db_search_roots": [str(p) for p in db_search_roots],
            "explicit_db_paths": [str(p) for p in explicit_db_paths],
            "db_candidates": [str(p) for p in deep_candidates],
            "compatible_dbs": deep_compatible,
            "db_diagnostics": deep_reports,
        }
        print(json.dumps(payload, indent=2))
        return 0

    if args.diagnose:
        payload = {
            "mode": args.mode,
            "codex_home": str(codex_home),
            "resolved_sqlite_home": str(sqlite_home) if sqlite_home else None,
            "db_search_roots": [str(p) for p in db_search_roots],
            "explicit_db_paths": [str(p) for p in explicit_db_paths],
            "db_candidates": [str(p) for p in db_candidates],
            "db_diagnostics": db_diagnostics,
            "compatible_dbs": [str(p) for p in db_paths],
        }
        print(json.dumps(payload, indent=2))
        return 0

    db_ids = ids if args.scope == "ids" else set()
    db_old_counts = {str(p): db_count_cwd(p, old, db_ids) for p in db_paths}
    db_new_counts = {str(p): db_count_cwd(p, new, db_ids) for p in db_paths}

    global_state_would_change = update_global_state_json(codex_home, old, new, False, None) if args.update_global_state else False

    summary = {
        "mode": args.mode,
        "scope": args.scope,
        "old": old,
        "new": new,
        "codex_home": str(codex_home),
        "resolved_sqlite_home": str(sqlite_home) if sqlite_home else None,
        "db_search_roots": [str(p) for p in db_search_roots],
        "jsonl": {
            "files_scanned": len(all_jsonl),
            "files_affected": len(jsonl_edits),
            "old_hits": sum(e.old_hits for e in jsonl_edits),
            "new_hits": sum(e.new_hits for e in jsonl_edits),
        },
        "state_db": {
            "db_candidates": len(db_candidates),
            "dbs": len(db_paths),
            "old_count_total": sum(db_old_counts.values()),
            "new_count_total": sum(db_new_counts.values()),
            "candidate_paths": [str(p) for p in db_candidates],
            "db_paths": [str(p) for p in db_paths],
        },
        "global_state_would_change": bool(global_state_would_change),
    }

    print(json.dumps(summary, indent=2))

    if not do_apply:
        return 0

    if len(db_paths) == 0 and len(jsonl_edits) > 0 and not args.allow_jsonl_only:
        eprint(
            "ERROR: JSONL cwd hits were found, but no compatible state DBs were discovered. "
            "Run with --diagnose (and optionally --db-path) to locate the active SQLite state DB, "
            "or rerun with --allow-jsonl-only to proceed intentionally."
        )
        return 3

    backup_dir = make_backup_dir(codex_home)

    backed_up: Set[Path] = set()
    for e in jsonl_edits:
        if e.path not in backed_up:
            backup_file(e.path, backup_dir, codex_home)
            backed_up.add(e.path)

    for db in db_paths:
        if db not in backed_up:
            backup_file(db, backup_dir, codex_home)
            backed_up.add(db)

    if args.update_global_state:
        update_global_state_json(codex_home, old, new, True, backup_dir)

    for e in jsonl_edits:
        text = e.path.read_text(encoding="utf-8", errors="ignore")
        updated = replace_cwd_hits(text, old, new)
        if updated != text:
            e.path.write_text(updated, encoding="utf-8")

    db_results = [apply_db_update(db, old, new, db_ids) for db in db_paths]

    post_jsonl = discover_jsonl_edits(all_jsonl, old, new)
    post_db_old = {str(p): db_count_cwd(p, old, db_ids) for p in db_paths}
    post_db_new = {str(p): db_count_cwd(p, new, db_ids) for p in db_paths}

    post = {
        "backup_dir": str(backup_dir),
        "jsonl": {
            "remaining_old_files": len(post_jsonl),
            "remaining_old_hits": sum(e.old_hits for e in post_jsonl),
        },
        "state_db": {
            "old_count_total": sum(post_db_old.values()),
            "new_count_total": sum(post_db_new.values()),
            "db_results": [
                {
                    "db": str(r.path),
                    "old_before": r.old_count_before,
                    "new_before": r.new_count_before,
                    "old_after": r.old_count_after,
                    "new_after": r.new_count_after,
                }
                for r in db_results
            ],
        },
    }
    print(json.dumps(post, indent=2))

    manifest = {
        "summary_pre": summary,
        "summary_post": post,
        "backed_up_files": [str(p) for p in sorted(backed_up)],
    }
    (backup_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
