# Hermes Kanban — Multi-Agent Pipeline Orchestration

A markdown-driven, multi-agent task orchestration system for Hermes Agent.
Define agent personas in `soul/`, pipeline stages in `pipelines/`, and let the
orchestrator decompose, assign, and track work across specialized agents.

## Quick Start

```bash
# Run the marketing pipeline
hermes kanban create "Marketing Campaign" --template pipelines/marketing.md

# Or use the orchestrator directly
python3 orchestrator.py pipelines/marketing.md

# Check board status
hermes kanban list
hermes kanban show <task_id>
```

## Architecture

```
soul/           → Agent persona definitions (researcher, analyst, writer, reviewer)
pipelines/      → Pipeline stage definitions (marketing, dev, content)
templates/      → Reusable task templates
orchestrator.py → Python orchestrator that reads pipelines and creates kanban tasks
```

## Agent Roles

| Agent | File | Role |
|-------|------|------|
| Researcher | `soul/researcher.md` | Audience research, data gathering |
| Analyst | `soul/analyst.md` | Messaging, positioning, strategy |
| Writer | `soul/writer.md` | Content creation (all formats) |
| Reviewer | `soul/reviewer.md` | Quality assurance, consistency check |

## Pipeline Format

Pipelines are markdown files with tasks defined as:

```markdown
## Task N

**Title:** Task title
**Assignee:** agent-role
**Depends On:** Task N, Task N (or "None")
**Description:** What the agent should do
**Output:** Expected output format
**Acceptance Criteria:**
- Criterion 1
- Criterion 2
```

## How It Works

1. **Orchestrator** reads the pipeline markdown
2. **Decomposes** into a dependency graph
3. **Creates** kanban tasks via `kanban_create` with proper parent links
4. **Dispatches** to worker profiles automatically
5. **Tracks** progress through the board
6. **Reports** completion with full audit trail

## Integration

This system uses the built-in Hermes Kanban toolset:
- `kanban_create` — create tasks with dependency links
- `kanban_complete` — mark done with structured handoff metadata
- `kanban_block` — pause for human input
- `kanban_comment` — add context to tasks
- `kanban_show` — read task state

## License

MIT
