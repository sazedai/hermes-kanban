---
title: Goal Mode
created: 2026-06-05
updated: 2026-06-05
type: concept
tags: [goal-mode, workflow, agent, orchestration]
sources: []
confidence: medium
---

# Goal Mode

Goal mode is an autonomous execution pattern in [[hermes-agent]] where a [[sub-agent]] (or the parent agent) is given a clear objective and runs until that objective is achieved, rather than stopping after a single tool call or response.

## Characteristics

- **Objective-driven** — the agent is given a goal, not a step-by-step procedure
- **Self-directed** — the agent decides which tools to call and in what order
- **Persistent** — the agent continues iterating until the goal is met or it determines the goal is impossible
- **Summary-oriented** — the agent produces a final summary of what it accomplished

## How It Differs from Step-by-Step

| Step-by-Step | Goal Mode |
|--------------|-----------|
| User specifies each action | User specifies the desired outcome |
| Agent stops after each step | Agent runs until completion |
| Tight human-in-the-loop | Autonomous execution |
| Good for simple, known procedures | Good for complex, exploratory tasks |

## When to Use Goal Mode

- **Research tasks** — "Investigate X and report findings"
- **Build tasks** — "Create a working implementation of Y"
- **Analysis tasks** — "Analyze this data and identify patterns"
- **Multi-step workflows** — any task requiring more than 2-3 tool calls

## Implementation in Sub-Agents

When [[delegate-task]] is used, the sub-agent inherently operates in goal mode: it receives a task description and runs until it has produced a summary. The parent agent does not micromanage the sub-agent's steps.

This is enabled by [[context-isolation]] — the sub-agent has a clean context to reason through the problem without distraction.

## Best Practices

- **Be specific about the goal** — vague goals produce vague results
- **Specify the output format** — tell the agent what the summary should look like
- **Set appropriate timeouts** — goal-mode agents may need many iterations
- **Include constraints** — "don't modify production files", "use only these tools"

## See Also

- [[sub-agent]] — the primary user of goal mode
- [[delegate-task]] — the tool that triggers goal-mode execution
- [[hermes-agent]] — the system that supports goal mode
- [[context-isolation]] — clean context helps goal-mode agents focus
- [[parallel-execution]] — goal-mode agents can run in parallel
