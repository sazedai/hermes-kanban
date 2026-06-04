---
title: Context Isolation
created: 2026-06-05
updated: 2026-06-05
type: concept
tags: [context-window, token-optimization, sub-agent]
sources: []
confidence: medium
---

# Context Isolation

Context isolation is the principle that each [[sub-agent]] operates within its own independent context window, receiving no inherited conversation history from the parent agent. Only the explicitly provided instruction text is available at startup.

## Why It Matters

Large language models have finite context windows. When a parent agent has accumulated many tool calls, results, and reasoning steps, delegating a task without isolation would mean:

- The sub-agent inherits irrelevant conversation history
- Token budget is wasted on prior context unrelated to the task
- Signal-to-noise ratio decreases, degrading output quality
- Risk of the sub-agent being influenced by misleading prior context

## How It Works

When [[delegate-task]] is called:

1. A fresh context window is allocated for the sub-agent
2. Only the prompt/instruction text is loaded
3. The sub-agent has no awareness of the parent's conversation
4. Tool results accumulate only within the sub-agent's own context
5. The parent reads only the final summary output

## Trade-offs

**Benefits:**
- Clean, task-focused reasoning for each sub-agent
- Maximum usable token budget for actual work
- Parent context stays lean across many delegations
- Reduced risk of context poisoning or prompt leakage

**Costs:**
- Sub-agents cannot reference parent conversation ("what did we discuss earlier?")
- Shared context must be explicitly copied into the instruction text
- Coordination between sub-agents requires explicit file-based communication

## Pattern: Briefing Document

A common pattern is to write a "briefing" section in the sub-agent's prompt that captures all needed context from the parent:

```
## Background
The user asked about X. Previous research found Y.
Focus this investigation specifically on Z.
```

This gives the sub-agent the signal without the noise.

## Relationship to Other Concepts

- Enabled by the [[delegate-task]] tool
- Prerequisite for effective [[parallel-execution]] (each parallel agent is isolated)
- Complements [[goal-mode]] — isolated agents with clear goals produce better results
- Core design principle of the [[hermes-agent]] architecture

## See Also

- [[sub-agent]] — the entity that benefits from isolation
- [[delegate-task]] — the mechanism that creates isolated contexts
- [[parallel-execution]] — isolation enables safe parallelism
- [[hermes-agent]] — the system designed around this principle
