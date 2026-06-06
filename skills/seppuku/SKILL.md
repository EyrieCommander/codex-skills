---
name: seppuku
description: "Use when the user invokes /seppuku, says a Codex thread should delete itself, self-archive, end itself, retire itself, stop permanently, or when a heartbeat/automation/thread is explicitly told to terminate its own conversation rather than continue. This skill performs a clean self-termination: stop work, preserve only essential handoff/evidence, avoid further action, and archive the current thread when supported."
---

# Seppuku

Use this skill as a deliberate self-termination path for the current Codex thread. Its job is not to fix the thread; its job is to stop the thread cleanly and remove it from active attention.

## Trigger

Run this only when the user explicitly invokes `/seppuku`, asks for the thread to delete/archive/end itself, or tells a heartbeat/automation/thread to retire its own conversation. Do not infer this from ordinary errors, weak output, or frustration unless the user clearly requests self-termination.

## Procedure

1. Stop all main work immediately.
2. Do not start new investigation unless it is required to preserve a minimal handoff.
3. If there is important unfinished state, write a short handoff in the final response:
   - current goal
   - last reliable evidence/source checked
   - known blockers
   - one suggested next safe action
4. If the thread belongs to a recurring automation or heartbeat, say whether the automation itself still needs pausing/deleting separately. Do not mutate automation state unless the user explicitly approved that exact action in the current turn.
5. Archive the current conversation using the supported archive mechanism.

## Archive Mechanism

When the current environment supports the `::archive{...}` directive, end the final response with:

```text
::archive{reason="User invoked /seppuku for this thread"}
```

If a true delete-thread tool exists in the current environment and the user explicitly requested deletion rather than archiving, use that instead of archive. Otherwise, be honest: archive is the available self-removal behavior.

## Do Not

- Do not keep working after `/seppuku`.
- Do not ask clarifying questions unless archiving would destroy data or the user's request is ambiguous about which thread should end.
- Do not delete files, sessions, logs, worktrees, skills, memories, or automations unless the user separately approves that exact destructive action.
- Do not post to GitHub or mutate project/public state.
