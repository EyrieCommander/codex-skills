#!/usr/bin/env python3
"""Smoke tests for keep-codex-fast using a fake Codex home."""

from __future__ import annotations

import argparse
import contextlib
import io
import importlib.util
import json
import os
import shlex
import sqlite3
import sys
import tempfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "keep_codex_fast.py"


def load_module():
    spec = importlib.util.spec_from_file_location("keep_codex_fast", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules["keep_codex_fast"] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    module.codex_processes_running = lambda: []
    module.top_node_processes = lambda details=False: module.report("top_node_processes skipped_in_smoke")
    return module


def make_fake_home(root: Path) -> dict[str, Path]:
    codex_home = root / ".codex"
    sessions = codex_home / "sessions" / "2026" / "01" / "01"
    sessions.mkdir(parents=True)
    rollout = sessions / "rollout-2026-01-01T00-00-00-aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa.jsonl"
    rollout.write_text('{"type":"test"}\n', encoding="utf-8")
    old_time = time.time() - 30 * 86400
    os.utime(rollout, (old_time, old_time))

    (codex_home / ".codex-global-state.json").write_text('{"pinned-thread-ids":[]}', encoding="utf-8")
    (codex_home / "config.toml").write_text(
        '[projects."C:\\\\DefinitelyMissingKeepCodexFast"]\n'
        'trust_level = "trusted"\n'
        '[plugins.keep-codex-fast]\n'
        r"source = '\\?\C:\Users\Tester\.codex\skills\keep-codex-fast'" + "\n",
        encoding="utf-8",
    )

    worktree = codex_home / "worktrees" / "oldtree"
    worktree.mkdir(parents=True)
    (worktree / "file.txt").write_text("x", encoding="utf-8")
    os.utime(worktree, (old_time, old_time))

    log_file = codex_home / "logs_2.sqlite"
    log_file.write_text("log", encoding="utf-8")
    tui_log_file = codex_home / "log" / "codex-tui.log"
    tui_log_file.parent.mkdir(parents=True)
    tui_log_file.write_text("tui log", encoding="utf-8")

    state_db = codex_home / "state_5.sqlite"
    conn = sqlite3.connect(state_db)
    conn.execute(
        "create table threads (id text primary key, title text, first_user_message text, rollout_path text, cwd text, created_at integer, updated_at integer, archived_at integer, archived integer)"
    )
    long_title = "Title " + ("x" * 300)
    long_preview = "Preview " + ("y" * 600)
    conn.execute(
        "insert into threads values (?,?,?,?,?,?,?,?,?)",
        (
            "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            long_title,
            long_preview,
            str(rollout),
            r"\\?\C:\DefinitelyMissingKeepCodexFast",
            int(old_time),
            int(old_time),
            None,
            0,
        ),
    )
    conn.commit()
    conn.close()

    return {
        "codex_home": codex_home,
        "rollout": rollout,
        "worktree": worktree,
        "log_file": log_file,
        "tui_log_file": tui_log_file,
        "state_db": state_db,
    }


def make_malformed_local_task_home(root: Path, *, include_archived_column: bool = True) -> dict[str, Path]:
    codex_home = root / ".codex"
    sessions = codex_home / "sessions" / "2026" / "01" / "01"
    sessions.mkdir(parents=True)
    malformed_rollout = sessions / "rollout-2026-01-01T00-00-00-bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb.jsonl"
    temp_rollout = sessions / "rollout-2026-01-01T00-00-00-dddddddd-dddd-dddd-dddd-dddddddddddd.jsonl"
    normal_rollout = sessions / "rollout-2026-01-01T00-00-01-cccccccc-cccc-cccc-cccc-cccccccccccc.jsonl"
    malformed_rollout.write_text('{"type":"malformed"}\n', encoding="utf-8")
    temp_rollout.write_text('{"type":"temp"}\n', encoding="utf-8")
    normal_rollout.write_text('{"type":"normal"}\n', encoding="utf-8")

    (codex_home / ".codex-global-state.json").write_text('{"pinned-thread-ids":[]}', encoding="utf-8")
    state_db = codex_home / "state_5.sqlite"
    conn = sqlite3.connect(state_db)
    if include_archived_column:
        conn.execute(
            """
            create table threads (
                id text primary key,
                title text,
                first_user_message text,
                rollout_path text,
                cwd text,
                updated_at integer,
                archived_at integer,
                archived integer,
                has_user_event integer
            )
            """
        )
        insert_sql = "insert into threads values (?,?,?,?,?,?,?,?,?)"
        malformed_values = (
            "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
            "<codex reminder>You are operating in text only mode.",
            "",
            str(malformed_rollout),
            "/",
            int(time.time()),
            None,
            0,
            0,
        )
        normal_values = (
            "cccccccc-cccc-cccc-cccc-cccccccccccc",
            "Normal user thread",
            "Normal user thread",
            str(normal_rollout),
            "/",
            int(time.time()),
            None,
            0,
            1,
        )
        temp_values = (
            "dddddddd-dddd-dddd-dddd-dddddddddddd",
            "You are the Discover agent.",
            "",
            str(temp_rollout),
            "/private/var/folders/aa/bb/T",
            int(time.time()),
            None,
            0,
            0,
        )
    else:
        conn.execute(
            """
            create table threads (
                id text primary key,
                title text,
                first_user_message text,
                rollout_path text,
                cwd text,
                updated_at integer,
                archived_at integer,
                has_user_event integer
            )
            """
        )
        insert_sql = "insert into threads values (?,?,?,?,?,?,?,?)"
        malformed_values = (
            "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
            "<codex reminder>You are operating in text only mode.",
            "",
            str(malformed_rollout),
            "/",
            int(time.time()),
            None,
            0,
        )
        normal_values = (
            "cccccccc-cccc-cccc-cccc-cccccccccccc",
            "Normal user thread",
            "Normal user thread",
            str(normal_rollout),
            "/",
            int(time.time()),
            None,
            1,
        )
        temp_values = (
            "dddddddd-dddd-dddd-dddd-dddddddddddd",
            "You are the Discover agent.",
            "",
            str(temp_rollout),
            "/private/var/folders/aa/bb/T",
            int(time.time()),
            None,
            0,
        )
    conn.execute(insert_sql, malformed_values)
    conn.execute(insert_sql, normal_values)
    conn.execute(insert_sql, temp_values)
    conn.commit()
    conn.close()
    return {
        "codex_home": codex_home,
        "malformed_rollout": malformed_rollout,
        "temp_rollout": temp_rollout,
        "normal_rollout": normal_rollout,
        "state_db": state_db,
    }


def latest_session_index_name(codex_home: Path, thread_id: str) -> str | None:
    path = codex_home / "session_index.jsonl"
    if not path.exists():
        return None
    name = None
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if record.get("id") == thread_id and record.get("thread_name"):
            name = record["thread_name"]
    return name


def assert_report_mode(module) -> None:
    with tempfile.TemporaryDirectory() as td:
        paths = make_fake_home(Path(td))
        backup = Path(td) / "backup-report"
        args = argparse.Namespace(
            apply=False,
            backup_only=False,
            details=False,
            wait_for_codex_exit=False,
            codex_home=str(paths["codex_home"]),
            backup_root=str(backup),
            archive_older_than_days=10,
            archive_age_field="updated_at",
            archive_thread_id=[],
            archive_rollout_path=[],
            worktree_older_than_days=7,
            rotate_logs_above_mb=0,
            thread_title_limit=120,
            thread_preview_limit=240,
            repair_thread_metadata_bloat=False,
        )
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            assert module.run(args) == 0
        text = output.getvalue()
        assert paths["rollout"].exists(), "report mode must not move sessions"
        assert paths["worktree"].exists(), "report mode must not move worktrees"
        assert paths["log_file"].exists(), "report mode must not rotate logs"
        assert paths["tui_log_file"].exists(), "report mode must not rotate TUI logs"
        assert not backup.exists(), "report mode must not create backup artifacts"
        assert "codex_tui_log_mb" in text
        assert "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa" not in text
        assert str(paths["codex_home"]) not in text
        conn = sqlite3.connect(paths["state_db"])
        title, preview = conn.execute(
            "select title, first_user_message from threads where id=?",
            ("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",),
        ).fetchone()
        conn.close()
        assert len(title) > 120, "report mode must not trim titles"
        assert len(preview) > 240, "report mode must not trim previews"


def assert_backup_only_mode(module) -> None:
    with tempfile.TemporaryDirectory() as td:
        paths = make_fake_home(Path(td))
        backup = Path(td) / "backup-only"
        args = argparse.Namespace(
            apply=False,
            backup_only=True,
            details=False,
            wait_for_codex_exit=False,
            codex_home=str(paths["codex_home"]),
            backup_root=str(backup),
            archive_older_than_days=10,
            archive_age_field="updated_at",
            archive_thread_id=[],
            archive_rollout_path=[],
            worktree_older_than_days=7,
            rotate_logs_above_mb=0,
            thread_title_limit=120,
            thread_preview_limit=240,
            repair_thread_metadata_bloat=False,
        )
        assert module.run(args) == 0
        assert paths["rollout"].exists(), "backup-only mode must not move sessions"
        assert paths["worktree"].exists(), "backup-only mode must not move worktrees"
        assert paths["log_file"].exists(), "backup-only mode must not rotate logs"
        assert paths["tui_log_file"].exists(), "backup-only mode must not rotate TUI logs"
        assert (backup / "state_5.sqlite").exists()
        assert (backup / "config.toml").exists()
        assert not (backup / "moved-sessions.jsonl").exists()
        conn = sqlite3.connect(paths["state_db"])
        title, preview = conn.execute(
            "select title, first_user_message from threads where id=?",
            ("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",),
        ).fetchone()
        conn.close()
        assert len(title) > 120, "backup-only mode must not trim titles"
        assert len(preview) > 240, "backup-only mode must not trim previews"


def assert_session_alias_detection(module) -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        real_root = root / "real"
        alias_root = root / "alias"
        real_root.mkdir()
        try:
            alias_root.symlink_to(real_root, target_is_directory=True)
        except OSError:
            return

        paths = make_fake_home(real_root)
        alias_home = alias_root / ".codex"
        conn = module.sqlite_connect(alias_home / "state_5.sqlite", readonly=True)
        try:
            candidates = module.active_session_candidates(conn, alias_home, 10, "updated_at", [], [])
        finally:
            conn.close()
        assert len(candidates) == 1


def assert_extended_rollout_path_detection(module) -> None:
    if os.name != "nt":
        return

    with tempfile.TemporaryDirectory() as td:
        paths = make_fake_home(Path(td))
        extended_rollout = "\\\\?\\" + str(paths["rollout"])
        conn = sqlite3.connect(paths["state_db"])
        conn.execute(
            "update threads set rollout_path=? where id=?",
            (extended_rollout, "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
        )
        conn.commit()
        conn.close()

        conn = module.sqlite_connect(paths["state_db"], readonly=True)
        try:
            candidates = module.active_session_candidates(conn, paths["codex_home"], 10, "updated_at", [], [])
        finally:
            conn.close()

        assert len(candidates) == 1
        assert candidates[0].source == paths["rollout"]


def assert_extended_path_normalization_targets_path_fields_and_config(module) -> None:
    with tempfile.TemporaryDirectory() as td:
        paths = make_fake_home(Path(td))
        backup = Path(td) / "backup-normalize"
        extended_rollout = "\\\\?\\" + str(paths["rollout"])
        text_preview = r"this title discusses the \\?\ Windows prefix and should not be rewritten"
        text_title = r"how does \\?\C:\path syntax work?"
        (paths["codex_home"] / "session_index.jsonl").write_text(
            json.dumps(
                {
                    "id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                    "thread_name": r"friendly \\?\ discussion",
                    "updated_at": "2026-01-01T00:00:00.000Z",
                }
            )
            + "\n",
            encoding="utf-8",
        )
        conn = sqlite3.connect(paths["state_db"])
        conn.execute(
            "update threads set title=?, rollout_path=?, first_user_message=? where id=?",
            (text_title, extended_rollout, text_preview, "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
        )
        conn.commit()
        conn.close()

        args = argparse.Namespace(
            apply=True,
            backup_only=False,
            details=False,
            wait_for_codex_exit=False,
            codex_home=str(paths["codex_home"]),
            backup_root=str(backup),
            archive_older_than_days=9999,
            archive_age_field="updated_at",
            archive_thread_id=[],
            archive_rollout_path=[],
            worktree_older_than_days=9999,
            rotate_logs_above_mb=64,
            thread_title_limit=120,
            thread_preview_limit=240,
            repair_thread_metadata_bloat=False,
        )
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            assert module.run(args) == 0
        text = output.getvalue()
        assert "extended_paths threads.first_user_message" not in text
        assert "extended_paths threads.title" not in text
        assert "extended_paths threads.rollout_path 1" in text
        assert "extended_paths threads.cwd 1" in text
        assert "extended_paths_file config.toml 1" in text

        conn = sqlite3.connect(paths["state_db"])
        title, rollout_path, cwd, preview = conn.execute(
            "select title, rollout_path, cwd, first_user_message from threads where id=?",
            ("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",),
        ).fetchone()
        conn.close()
        assert title == text_title
        assert "\\\\?\\" not in rollout_path
        assert "\\\\?\\" not in cwd
        assert preview == text_preview
        config = (paths["codex_home"] / "config.toml").read_text(encoding="utf-8")
        assert "\\\\?\\" not in config
        assert r"C:\Users\Tester\.codex\skills\keep-codex-fast" in config
        session_index = (paths["codex_home"] / "session_index.jsonl").read_text(encoding="utf-8")
        session_index_record = json.loads(session_index)
        assert session_index_record["thread_name"] == r"friendly \\?\ discussion"


def assert_created_at_archive_field(module) -> None:
    with tempfile.TemporaryDirectory() as td:
        paths = make_fake_home(Path(td))
        now = int(time.time())
        old = now - 30 * 86400
        conn = sqlite3.connect(paths["state_db"])
        conn.execute(
            "update threads set created_at=?, updated_at=? where id=?",
            (old, now, "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
        )
        conn.commit()

        updated_candidates = module.active_session_candidates(
            conn,
            paths["codex_home"],
            10,
            "updated_at",
            [],
            [],
        )
        created_candidates = module.active_session_candidates(
            conn,
            paths["codex_home"],
            10,
            "created_at",
            [],
            [],
        )
        conn.close()

        assert updated_candidates == []
        assert len(created_candidates) == 1
        assert created_candidates[0].reason == "created_at_older_than_10d"


def assert_targeted_session_archive(module) -> None:
    with tempfile.TemporaryDirectory() as td:
        paths = make_fake_home(Path(td))
        now = int(time.time())
        conn = sqlite3.connect(paths["state_db"])
        conn.execute(
            "update threads set created_at=?, updated_at=? where id=?",
            (now, now, "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
        )
        conn.commit()

        candidates = module.active_session_candidates(
            conn,
            paths["codex_home"],
            10,
            "updated_at",
            ["aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"],
            [],
        )
        conn.close()

        assert len(candidates) == 1
        assert candidates[0].reason == "target_thread_id"


def assert_apply_mode(module) -> None:
    with tempfile.TemporaryDirectory() as td:
        paths = make_fake_home(Path(td))
        backup = Path(td) / "backup apply with spaces"
        (paths["codex_home"] / "session_index.jsonl").write_text(
            '{"id":"aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa","thread_name":"Friendly Agent","updated_at":"2026-01-01T00:00:00.000Z"}\n',
            encoding="utf-8",
        )
        args = argparse.Namespace(
            apply=True,
            backup_only=False,
            details=False,
            wait_for_codex_exit=False,
            codex_home=str(paths["codex_home"]),
            backup_root=str(backup),
            archive_older_than_days=10,
            archive_age_field="updated_at",
            archive_thread_id=[],
            archive_rollout_path=[],
            worktree_older_than_days=7,
            rotate_logs_above_mb=0,
            thread_title_limit=120,
            thread_preview_limit=240,
            repair_thread_metadata_bloat=True,
        )
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            assert module.run(args) == 0
        text = output.getvalue()

        conn = sqlite3.connect(paths["state_db"])
        archived, archived_at, rollout_path, cwd, title, preview = conn.execute(
            "select archived, archived_at, rollout_path, cwd, title, first_user_message from threads where id=?",
            ("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",),
        ).fetchone()
        conn.close()

        assert archived == 1
        assert archived_at is not None
        assert "archived_sessions" in rollout_path
        assert cwd == r"C:\DefinitelyMissingKeepCodexFast"
        assert title == "Friendly Agent"
        assert len(preview) <= 240
        assert not paths["rollout"].exists()
        assert not paths["worktree"].exists()
        assert not paths["log_file"].exists()
        assert not paths["tui_log_file"].exists()
        assert list((paths["codex_home"] / "archived_logs").glob("keep-codex-fast-*/codex-tui.log"))
        assert "DefinitelyMissingKeepCodexFast" not in (paths["codex_home"] / "config.toml").read_text(
            encoding="utf-8"
        )
        resolved_backup = backup.resolve()
        session_restore = resolved_backup / "restore-sessions.py"
        metadata_restore = resolved_backup / "restore-thread-metadata.py"
        assert session_restore.exists()
        assert metadata_restore.exists()
        assert os.access(session_restore, os.X_OK)
        assert os.access(metadata_restore, os.X_OK)
        assert f"session_restore_command python3 {shlex.quote(str(session_restore))}" in text
        assert f"thread_metadata_restore_command python3 {shlex.quote(str(metadata_restore))}" in text
        assert (backup / "moved-sessions.jsonl").exists()
        assert (backup / "thread-metadata-repairs.jsonl").exists()
        assert (backup / "moved-worktrees.jsonl").exists()
        assert latest_session_index_name(paths["codex_home"], "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa") == "Friendly Agent"


def assert_repair_adds_bounded_name_when_no_existing_name(module) -> None:
    with tempfile.TemporaryDirectory() as td:
        paths = make_fake_home(Path(td))
        backup = Path(td) / "backup-repair-name"
        args = argparse.Namespace(
            apply=True,
            backup_only=False,
            details=False,
            wait_for_codex_exit=False,
            codex_home=str(paths["codex_home"]),
            backup_root=str(backup),
            archive_older_than_days=10,
            archive_age_field="updated_at",
            archive_thread_id=[],
            archive_rollout_path=[],
            worktree_older_than_days=7,
            rotate_logs_above_mb=64,
            thread_title_limit=120,
            thread_preview_limit=240,
            repair_thread_metadata_bloat=True,
        )
        assert module.run(args) == 0
        name = latest_session_index_name(paths["codex_home"], "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
        assert name is not None
        assert len(name) <= 120


def assert_repair_restores_existing_name_when_title_is_already_bounded(module) -> None:
    with tempfile.TemporaryDirectory() as td:
        paths = make_fake_home(Path(td))
        backup = Path(td) / "backup-repair-existing-name"
        conn = sqlite3.connect(paths["state_db"])
        conn.execute(
            "update threads set title=?, first_user_message=? where id=?",
            ("Short prompt fallback", "Short preview", "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
        )
        conn.commit()
        conn.close()
        (paths["codex_home"] / "session_index.jsonl").write_text(
            '{"id":"aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa","thread_name":"Friendly Agent","updated_at":"2026-01-01T00:00:00.000Z"}\n',
            encoding="utf-8",
        )
        args = argparse.Namespace(
            apply=True,
            backup_only=False,
            details=False,
            wait_for_codex_exit=False,
            codex_home=str(paths["codex_home"]),
            backup_root=str(backup),
            archive_older_than_days=10,
            archive_age_field="updated_at",
            archive_thread_id=[],
            archive_rollout_path=[],
            worktree_older_than_days=7,
            rotate_logs_above_mb=64,
            thread_title_limit=120,
            thread_preview_limit=240,
            repair_thread_metadata_bloat=True,
        )
        assert module.run(args) == 0
        conn = sqlite3.connect(paths["state_db"])
        title = conn.execute(
            "select title from threads where id=?",
            ("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",),
        ).fetchone()[0]
        conn.close()
        assert title == "Friendly Agent"


def assert_normal_apply_does_not_repair_thread_metadata(module) -> None:
    with tempfile.TemporaryDirectory() as td:
        paths = make_fake_home(Path(td))
        backup = Path(td) / "backup-normal-apply"
        args = argparse.Namespace(
            apply=True,
            backup_only=False,
            details=False,
            wait_for_codex_exit=False,
            codex_home=str(paths["codex_home"]),
            backup_root=str(backup),
            archive_older_than_days=10,
            archive_age_field="updated_at",
            archive_thread_id=[],
            archive_rollout_path=[],
            worktree_older_than_days=7,
            rotate_logs_above_mb=64,
            thread_title_limit=120,
            thread_preview_limit=240,
            repair_thread_metadata_bloat=False,
        )
        assert module.run(args) == 0

        conn = sqlite3.connect(paths["state_db"])
        title, preview = conn.execute(
            "select title, first_user_message from threads where id=?",
            ("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",),
        ).fetchone()
        conn.close()

        assert len(title) > 120, "normal apply must not trim titles without explicit repair flag"
        assert len(preview) > 240, "normal apply must not trim previews without explicit repair flag"
        assert not (backup / "thread-metadata-repairs.jsonl").exists()
        assert not (backup / "restore-thread-metadata.py").exists()


def assert_malformed_local_task_report_mode(module) -> None:
    with tempfile.TemporaryDirectory() as td:
        paths = make_malformed_local_task_home(Path(td))
        args = argparse.Namespace(
            apply=False,
            backup_only=False,
            details=False,
            wait_for_codex_exit=False,
            codex_home=str(paths["codex_home"]),
            backup_root=str(Path(td) / "backup-report"),
            archive_older_than_days=10,
            archive_age_field="updated_at",
            archive_thread_id=[],
            archive_rollout_path=[],
            worktree_older_than_days=7,
            rotate_logs_above_mb=64,
            thread_title_limit=120,
            thread_preview_limit=240,
            repair_thread_metadata_bloat=False,
            archive_malformed_local_tasks=False,
        )
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            assert module.run(args) == 0
        text = output.getvalue()
        assert "malformed_local_task_candidates 2" in text
        assert "malformed_local_task_root_cwd 1" in text
        assert "malformed_local_task_temp_cwd 1" in text
        assert paths["malformed_rollout"].exists()
        assert paths["temp_rollout"].exists()
        assert paths["normal_rollout"].exists()


def assert_malformed_local_task_archive_is_explicit(module) -> None:
    with tempfile.TemporaryDirectory() as td:
        paths = make_malformed_local_task_home(Path(td))
        backup = Path(td) / "backup-apply"
        args = argparse.Namespace(
            apply=True,
            backup_only=False,
            details=False,
            wait_for_codex_exit=False,
            codex_home=str(paths["codex_home"]),
            backup_root=str(backup),
            archive_older_than_days=99999,
            archive_age_field="updated_at",
            archive_thread_id=[],
            archive_rollout_path=[],
            worktree_older_than_days=99999,
            rotate_logs_above_mb=64,
            thread_title_limit=120,
            thread_preview_limit=240,
            repair_thread_metadata_bloat=False,
            archive_malformed_local_tasks=False,
        )
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            assert module.run(args) == 0
        assert "malformed_local_task_archive skipped_flag_required" in output.getvalue()
        assert paths["malformed_rollout"].exists()
        assert paths["temp_rollout"].exists()


def assert_malformed_local_task_archive_mode(module) -> None:
    with tempfile.TemporaryDirectory() as td:
        paths = make_malformed_local_task_home(Path(td))
        backup = Path(td) / "backup-apply"
        args = argparse.Namespace(
            apply=True,
            backup_only=False,
            details=False,
            wait_for_codex_exit=False,
            codex_home=str(paths["codex_home"]),
            backup_root=str(backup),
            archive_older_than_days=99999,
            archive_age_field="updated_at",
            archive_thread_id=[],
            archive_rollout_path=[],
            worktree_older_than_days=99999,
            rotate_logs_above_mb=64,
            thread_title_limit=120,
            thread_preview_limit=240,
            repair_thread_metadata_bloat=False,
            archive_malformed_local_tasks=True,
        )
        assert module.run(args) == 0

        conn = sqlite3.connect(paths["state_db"])
        malformed = conn.execute(
            "select archived, archived_at, rollout_path from threads where id=?",
            ("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",),
        ).fetchone()
        normal = conn.execute(
            "select archived, archived_at, rollout_path from threads where id=?",
            ("cccccccc-cccc-cccc-cccc-cccccccccccc",),
        ).fetchone()
        temp = conn.execute(
            "select archived, archived_at, rollout_path from threads where id=?",
            ("dddddddd-dddd-dddd-dddd-dddddddddddd",),
        ).fetchone()
        conn.close()

        assert malformed[0] == 1
        assert malformed[1] is not None
        assert "archived_sessions" in malformed[2]
        assert temp[0] == 1
        assert temp[1] is not None
        assert "archived_sessions" in temp[2]
        assert normal[0] == 0
        assert normal[1] is None
        assert paths["normal_rollout"].exists()
        assert not paths["malformed_rollout"].exists()
        assert not paths["temp_rollout"].exists()
        assert (backup / "moved-malformed-local-tasks.jsonl").exists()
        assert (backup / "restore-malformed-local-tasks.py").exists()
        assert not (backup / "restore-sessions.py").exists()


def assert_malformed_local_task_archive_without_archived_column(module) -> None:
    with tempfile.TemporaryDirectory() as td:
        paths = make_malformed_local_task_home(Path(td), include_archived_column=False)
        backup = Path(td) / "backup-apply"
        args = argparse.Namespace(
            apply=True,
            backup_only=False,
            details=False,
            wait_for_codex_exit=False,
            codex_home=str(paths["codex_home"]),
            backup_root=str(backup),
            archive_older_than_days=99999,
            archive_age_field="updated_at",
            archive_thread_id=[],
            archive_rollout_path=[],
            worktree_older_than_days=99999,
            rotate_logs_above_mb=64,
            thread_title_limit=120,
            thread_preview_limit=240,
            repair_thread_metadata_bloat=False,
            archive_malformed_local_tasks=True,
        )
        assert module.run(args) == 0

        conn = sqlite3.connect(paths["state_db"])
        malformed = conn.execute(
            "select archived_at, rollout_path from threads where id=?",
            ("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",),
        ).fetchone()
        normal = conn.execute(
            "select archived_at, rollout_path from threads where id=?",
            ("cccccccc-cccc-cccc-cccc-cccccccccccc",),
        ).fetchone()
        conn.close()

        assert malformed[0] is not None
        assert "archived_sessions" in malformed[1]
        assert normal[0] is None

        restore = backup / "restore-malformed-local-tasks.py"
        assert restore.exists()
        namespace = {"__name__": "__main__"}
        exec(restore.read_text(encoding="utf-8"), namespace)

        conn = sqlite3.connect(paths["state_db"])
        restored = conn.execute(
            "select archived_at, rollout_path from threads where id=?",
            ("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",),
        ).fetchone()
        conn.close()
        assert restored[0] is None
        assert restored[1] == str(paths["malformed_rollout"])
        assert paths["malformed_rollout"].exists()


def main() -> int:
    module = load_module()
    assert_report_mode(module)
    assert_backup_only_mode(module)
    assert_session_alias_detection(module)
    assert_extended_rollout_path_detection(module)
    assert_extended_path_normalization_targets_path_fields_and_config(module)
    assert_created_at_archive_field(module)
    assert_targeted_session_archive(module)
    assert_normal_apply_does_not_repair_thread_metadata(module)
    assert_malformed_local_task_report_mode(module)
    assert_malformed_local_task_archive_is_explicit(module)
    assert_malformed_local_task_archive_mode(module)
    assert_malformed_local_task_archive_without_archived_column(module)
    assert_repair_adds_bounded_name_when_no_existing_name(module)
    assert_repair_restores_existing_name_when_title_is_already_bounded(module)
    assert_apply_mode(module)
    print("smoke tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
