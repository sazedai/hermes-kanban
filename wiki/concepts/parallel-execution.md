---
title: Parallel Execution
created: 2026-06-05
updated: 2026-06-05
type: concept
tags: [parallel-execution, orchestration, workflow, delegation]
sources: []
confidence: medium
---

# Parallel Execution

Parallel execution in [[hermes-agent]] means spawning multiple [[sub-agent]]s simultaneously via [[delegate-task]] to work on independent tasks concurrently, rather than sequentially.

## Why Parallelize

Sequential task execution is simple but slow. When tasks are independent — meaning one task's output isn't another's input — running them in parallel can dramatically reduce wall-clock time.

Example: Researching 5 topics sequentially might take 25 minutes. In parallel, the same work might take only 6 minutes (bounded by the slowest single task).

## How It Works

1. The parent agent identifies independent subtasks
2. Multiple `delegate_task` calls are made in rapid succession (same tool-call round)
3. Sub-agents execute concurrently (provider-dependent parallelism)
4. Each sub-agent writes its summary to a designated output path
5. The parent collects and synthesizes results once all complete

## Requirements for Safe Parallelism

- **Task independence** — no sub-agent depends on another's output
- **[[context-isolation]]** — each sub-agent has its own context (no shared state)
- **File-based communication** — sub-agents communicate via files, not direct messaging
- **Idempotent writes** — each sub-agent writes to its own output file (no conflicts)

## Fan-Out / Fan-In Pattern

The most common parallel pattern:

```
Parent
  |-- delegate_task("Research topic A") --> writes to /tmp/a.md
  |-- delegate_task("Research topic B") --> writes to /tmp/b.md
  |-- delegate_task("Research topic C") --> writes to /tmp/c.md
  |
  v (after all complete)
Parent reads /tmp/a.md, /tmp/b.md, /tmp/c.md
Parent synthesizes into final output
```

## Limitations

- Provider rate limits may throttle true parallelism
- Each sub-agent consumes its own token budget
- Debugging parallel failures is harder than sequential
- Not all tasks are parallelizable (dependencies exist)

## See Also

- [[sub-agent]] — the unit of parallel work
- [[delegate-task]] — the tool that spawns parallel agents
- [[context-isolation]] — required for safe parallelism
- [[hermes-agent]] — the orchestrator enabling this pattern
- [[goal-mode]] — the execution model each parallel agent uses
