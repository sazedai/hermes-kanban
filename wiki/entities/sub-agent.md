---
title: Sub-Agent
created: 2026-06-05
updated: 2026-06-05
type: entity
tags: [sub-agent, delegation, orchestration]
sources: []
confidence: medium
---

# Sub-Agent

A sub-agent is a child AI agent spawned by a parent agent (e.g., [[hermes-agent]]) to perform a specific, bounded task in its own isolated context. Sub-agents inherit no context from the parent beyond what is explicitly provided in the instruction text.

## Purpose

Sub-agents exist to:

1. **Isolate context** — prevent task-specific tokens from polluting the parent's context window ([[context-isolation]])
2. **Enable parallelism** — run multiple tasks simultaneously ([[parallel-execution]])
3. **Specialize** — give a sub-agent a specific role, toolset, or perspective
4. **Contain failure** — a failed sub-agent doesn't corrupt the parent's state

## Lifecycle

1. Parent calls [[delegate-task]] with instruction text and parameters
2. Sub-agent starts with a clean context (no parent history)
3. Sub-agent executes autonomously, using tools as needed
4. Sub-agent writes a summary to the specified output path
5. Parent reads the summary and continues

## Identity

A sub-agent carries an identity (name, role, or label) that appears in logs and can be used for tracking and debugging. Sub-agents can themselves spawn sub-agents, forming an n-level delegation tree, though in practice 2 levels is the norm.

## Limitations

- Sub-agents cannot communicate with each other directly
- Sub-agents only report back to their parent via file output
- A sub-agents token budget is independent but finite
- Sub-agents should NOT assume prior context beyond their instructions

## See Also

- [[hermes-agent]] — the primary agent that spawns sub-agents
- [[delegate-task]] — the tool used to create sub-agents
- [[context-isolation]] — the model explaining context separation
- [[parallel-execution]] — how multiple sub-agents run simultaneously
- [[goal-mode]] — autonomous execution model used by sub-agents
