# Task Template — Copy and customize

## Task N

**Title:** [Clear, action-oriented title]
**Assignee:** [researcher | analyst | writer | reviewer]
**Depends On:** [Task N, Task N | None]
**Description:** [What the agent should do. Be specific about the approach, constraints, and context.]
**Output:** [Expected output format — document, code, analysis, etc.]
**Acceptance Criteria:**
- [Measurable criterion 1]
- [Measurable criterion 2]
- [Measurable criterion 3]

## Assignee Roles

- **researcher** — Gathers data, synthesizes insights, produces briefs
- **analyst** — Interprets data, makes strategic decisions, defines frameworks
- **writer** — Creates content in any format (copy, code, docs, scripts)
- **reviewer** — Quality assurance, consistency checks, security review

## Dependency Rules

1. Always specify dependencies explicitly
2. Use "None" for root tasks (no dependencies)
3. Multiple dependencies: "Task 1, Task 2"
4. The orchestrator will auto-level tasks based on dependencies
5. Tasks at the same level with no inter-dependencies run in parallel

## Pipeline Best Practices

- Keep tasks atomic — one clear output per task
- Write acceptance criteria that a reviewer can objectively check
- Include enough context in the description for a fresh agent to start
- Use the messaging framework pattern: analyst defines → writer creates → reviewer checks
- For long-running tasks, add estimated time in the description
