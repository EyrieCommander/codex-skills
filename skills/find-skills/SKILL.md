---
name: find-skills
description: Use when the user asks how to do a specialized task, asks whether a skill/tool exists, wants to extend agent capabilities, or a task looks like a repeated workflow that might benefit from an existing installable skill.
---

# Find Skills

This skill helps discover skills from the local and open agent skills ecosystem.

Core rule: scout for skills often, install carefully. It is good for agents to search for skills whenever a task looks specialized, repeatable, or likely to have an existing workflow. Skill discovery is low-risk; global installation is not.

## When to Use This Skill

Use this skill when the user:

- Asks "how do I do X" where X might be a common task with an existing skill
- Says "find a skill for X" or "is there a skill for X"
- Asks "can you do X" where X is a specialized capability
- Expresses interest in extending agent capabilities
- Wants to search for tools, templates, or workflows
- Mentions they wish they had help with a specific domain (design, testing, deployment, etc.)
- Repeats a workflow that may deserve a reusable skill

Do not let skill discovery block obvious work. If the task is urgent or straightforward, do the work and mention any promising skill follow-up afterward.

## What is the Skills CLI?

The Skills CLI (`npx skills`) is the package manager for the open agent skills ecosystem. Skills are modular packages that extend agent capabilities with specialized knowledge, workflows, and tools.

**Key commands:**

- `npx skills find [query]` - Search for skills interactively or by keyword
- `npx skills add <package>` - Install a skill from GitHub or other sources
- `npx skills check` - Check for skill updates
- `npx skills update` - Update all installed skills

**Browse skills at:** https://skills.sh/

## How to Help Users Find Skills

### Step 1: Understand What They Need

When a user asks for help with something, identify:

1. The domain (e.g., React, testing, design, deployment)
2. The specific task (e.g., writing tests, creating animations, reviewing PRs)
3. Whether this is a common enough task that a skill likely exists

### Step 2: Check Local Skills First

Before searching the public ecosystem, check skills already available to the agent:

1. Session-provided skills in the current skill list
2. User-level Codex skills, usually `~/.codex/skills`
3. User-level agent skills, usually `~/.agents/skills`
4. Project-local skills, if the current repo has a `skills/` directory

If a local skill already fits, use it instead of installing another one.

### Step 3: Check the Leaderboard

Before running a CLI search, check the [skills.sh leaderboard](https://skills.sh/) to see if a well-known skill already exists for the domain. The leaderboard ranks skills by total installs, surfacing the most popular and battle-tested options.

For example, top skills for web development include:
- `vercel-labs/agent-skills` — React, Next.js, web design (100K+ installs each)
- `anthropics/skills` — Frontend design, document processing (100K+ installs)

### Step 4: Search for Skills

If the leaderboard doesn't cover the user's need, run the find command:

```bash
npx skills find [query]
```

For example:

- User asks "how do I make my React app faster?" → `npx skills find react performance`
- User asks "can you help me with PR reviews?" → `npx skills find pr review`
- User asks "I need to create a changelog" → `npx skills find changelog`

### Step 5: Verify Quality Before Recommending

**Do not recommend a skill based solely on search results.** Always verify:

1. **Install count** — Treat installs as a signal, not a decision rule. Popular skills are often safer; new or niche skills may still be excellent.
2. **Source reputation** — Official sources (`vercel-labs`, `anthropics`, `microsoft`) are more trustworthy than unknown authors.
3. **GitHub stars and repo activity** — Check whether the source repository appears maintained.
4. **License** — Prefer clear permissive licenses when the skill may be reused or repackaged.
5. **Files included** — Inspect the skill contents before installing when possible.
6. **Safety boundary** — Be cautious with skills that ask for credentials, network access, shell scripts, browser automation, GitHub mutation, email, local state mutation, or global config changes.

### Step 6: Present Options to the User

When you find relevant skills, present them to the user with:

1. The skill name and what it does
2. The install count and source
3. The install command they can run
4. A link to learn more at skills.sh

Example response:

```
I found a skill that might help! The "react-best-practices" skill provides
React and Next.js performance optimization guidelines from Vercel Engineering.
(185K installs)

To install it:
npx skills add vercel-labs/agent-skills@react-best-practices

Learn more: https://skills.sh/vercel-labs/agent-skills/react-best-practices
```

### Step 7: Offer to Install

If the user wants to proceed, install only after explicit approval for that specific package and scope. Prefer showing what will be installed and where it will land before mutating global skill state.

```bash
npx skills add <owner/repo@skill> -g -y
```

The `-g` flag installs globally (user-level) and `-y` skips confirmation prompts. Use `-y` only when the user has already approved the exact package. If the CLI supports a local/project install, prefer that when the skill is project-specific.

After installing, verify the skill is visible to the relevant agent runtime. Codex and other agent harnesses may use different skill roots, commonly `~/.codex/skills` and `~/.agents/skills`.

## Common Skill Categories

When searching, consider these common categories:

| Category        | Example Queries                          |
| --------------- | ---------------------------------------- |
| Web Development | react, nextjs, typescript, css, tailwind |
| Testing         | testing, jest, playwright, e2e           |
| DevOps          | deploy, docker, kubernetes, ci-cd        |
| Documentation   | docs, readme, changelog, api-docs        |
| Code Quality    | review, lint, refactor, best-practices   |
| Design          | ui, ux, design-system, accessibility     |
| Productivity    | workflow, automation, git                |

## Tips for Effective Searches

1. **Use specific keywords**: "react testing" is better than just "testing"
2. **Try alternative terms**: If "deploy" doesn't work, try "deployment" or "ci-cd"
3. **Check popular sources**: Many skills come from `vercel-labs/agent-skills` or `ComposioHQ/awesome-claude-skills`

## When No Skills Are Found

If no relevant skills exist:

1. Acknowledge that no existing skill was found
2. Offer to help with the task directly using your general capabilities
3. Suggest the user could create their own skill with `npx skills init`

Example:

```
I searched for skills related to "xyz" but didn't find any matches.
I can still help you with this task directly! Would you like me to proceed?

If this is something you do often, you could create your own skill:
npx skills init my-xyz-skill
```
