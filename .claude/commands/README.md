# `.claude/commands/` — project commands

Project-scoped commands for **voice-seed**. They travel with the repo.

**Format:** one `<name>.md` per command — YAML frontmatter + markdown body.

| Command | What it does |
|---|---|
| [`voice-design.md`](voice-design.md) | Route writing voice by register → open owning SSOT → edit safely |

### Agent-agnostic

Plain markdown procedures. If the agent doesn’t auto-load `.claude/commands/`:

```
Read .claude/commands/voice-design.md and follow it
```
