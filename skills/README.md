# Skills

This directory contains installable Codex skill folders. Each ready skill is self-contained enough to copy into a local Codex skills directory.

Typical shape:

```text
skills/<skill-name>/SKILL.md
skills/<skill-name>/references/
skills/<skill-name>/agents/openai.yaml
```

`SKILL.md` is required. References, scripts, assets, tests, and `agents/openai.yaml` are optional, but should stay inside the skill folder they support.

Before adding a new skill here, update `CATALOG.md` with status and provenance, and check `NOTICE.md` for license or upstream attribution notes.
