---
title: Intelligent AI Delegation
created: 2026-06-05
updated: 2026-06-05
type: concept
tags: [delegation, multi-agent, trust, accountability]
sources: [raw/papers/2602.11865.md]
confidence: high
---

# Intelligent AI Delegation

**Paper**: arXiv:2602.11865 (February 2026)
**Authors**: Nenad Tomašev, Matija Franklin, Simon Osindero

## Summary
Proposes an adaptive framework for AI delegation that goes beyond simple heuristics. Addresses delegation as a sequence of decisions involving authority, responsibility, accountability, and trust.

## Key Concepts

### Seven Delegation Dimensions
1. **Task Allocation** — Which tasks to delegate and to whom
2. **Transfer of Authority** — Granting decision-making power
3. **Transfer of Responsibility** — Assigning ownership of outcomes
4. **Accountability** — Mechanisms for answerability
5. **Clear Role Specifications** — Defining roles and boundaries
6. **Clarity of Intent** — Well-communicated goals
7. **Trust Mechanisms** — Building trust between parties

### Problem with Current Approaches
Existing methods rely on simple heuristics and cannot:
- Dynamically adapt to environmental changes
- Robustly handle unexpected failures

## Relevance to Sub-Agent Delegation
This framework directly applies to [[sub-agent]] design in Hermes Agent. When using [[delegate_task]], the parent agent must provide clear role specifications, clarity of intent, and appropriate authority boundaries.

## Cross-References
- [[sub-agent]] — Sub-agent delegation in Hermes
- [[delegate-task]] — The delegate_task tool
- [[context-isolation]] — Why isolation matters for delegation
