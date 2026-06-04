---
title: Autonomy and Agency in Agentic AI
created: 2026-06-05
updated: 2026-06-05
type: concept
tags: [agent, autonomy, agency, multi-agent, compliance]
sources: [raw/papers/2605.12105.md]
confidence: high
---

# Autonomy and Agency in Agentic AI

**Paper**: arXiv:2605.12105 (May 2026)
**Authors**: Damir Safin, Dian Balta

## Summary
This paper introduces a structured framework for designing agentic AI systems in regulated environments by co-designing two dimensions: **agency** (what the system can do) and **autonomy** (how much it acts without human involvement).

## Key Concepts

### Two-Dimensional Design Space
Five operational levels for each dimension:
- **Autonomy L1→L5**: Human-commanded → Fully autonomous monitoring
- **Agency L1→L5**: Reasoning over context → Committed writes to records

### Six Architectural Tactics
1. **Checkpoints** — Human review points before critical actions
2. **Escalation** — Route high-risk decisions to humans
3. **Multi-agent delegation** — Distribute tasks with bounded authority
4. **Tool provisioning** — Grant access only to necessary tools
5. **Tool fencing** — Restrict tool usage by context/risk
6. **Write staging** — Buffer writes until validated

## Relevance to Sub-Agent Delegation
The "multi-agent delegation" tactic is directly relevant to [[sub-agent]] design. It provides principled guidance on bounding sub-agent authority — a key concern when designing [[delegate-task]] workflows.

## Cross-References
- [[sub-agent]] — Sub-agent delegation patterns
- [[context-isolation]] — Isolated context model
- [[goal-mode]] — Autonomous execution patterns
