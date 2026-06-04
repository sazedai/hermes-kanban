---
title: delegate_task
created: 2026-06-05
updated: 2026-06-05
type: entity
tags: [delegation, orchestration, workflow]
sources: []
confidence: medium
---

# delegate_task

The `delegate_task` tool is the primary mechanism in [[hermes-agent]] for spawning a [[sub-agent]] to perform work asynchronously or in parallel. It creates a new computational agent with its own identity, isolated context window, and instructions.

## Parameters

| Parameter | Purpose |
|-----------|---------|
| `prompt` | Instruction text for the sub-agent (the full task specification) |
| `label` | Human-readable label for logging and tracking |
| `model` | Optional model override for the sub-agent |
| `run_timeout_seconds` | Maximum wall-clock time before the sub-agent is terminated |

## Behavior

When `delegate_task` is invoked:

1. A new sub-agent process is created with a fresh context
2. The prompt text becomes the sub-agent's system + user message
3. The sub-agent runs until completion or timeout
4. The sub-agent writes its summary output
5. The tool call returns a reference to the spawned sub-agent

## Output Contract

Sub-agents typically write a structured summary file to a specified path. The parent agent reads this file to incorporate results. The output is plain Markdown — no binary data, no partial results.

## When to Use

- **Multiple independent tasks** — fan out work across parallel agents ([[parallel-execution]])
- **Context-heavy work** — isolate large investigations to keep the parent's context clean ([[context-isolation]])
- **Specialized research** — give a sub-agent a narrow focus with specific tool guidance
- **Iterative refinement** — chain sub-agents where each refines the previous output

## Best Practices

- Be explicit in prompts — sub-agents have no implicit context
- Specify the output format expected in the summary
- Set appropriate timeouts — long-running tasks need generous limits
- Cross-reference results in the wiki with [[wikilinks]]

## See Also

- [[sub-agent]] — the entity created by delegate_task
- [[hermes-agent]] — the agent that provides this tool
- [[context-isolation]] — why delegation isolates context
- [[parallel-execution]] — scaling via parallel sub-agents
- [[goal-mode]] — the autonomous execution model sub-agents use
