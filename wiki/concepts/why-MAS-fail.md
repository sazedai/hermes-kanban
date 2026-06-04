---
title: Why Multi-Agent LLM Systems Fail
created: 2026-06-05
updated: 2026-06-05
type: concept
tags: [multi-agent, failure-modes, taxonomy, MAS]
sources: [raw/papers/2503.13657.md]
confidence: high
---

# Why Do Multi-Agent LLM Systems Fail?

**Paper**: arXiv:2503.13657 (March 2025)
**Authors**: Mert Cemri et al. (UC Berkeley, Databricks)

## Summary
First comprehensive study of multi-agent LLM system (MAS) failures. Analyzes 7 popular MAS frameworks across 150+ tasks to identify systematic failure modes.

## Key Contributions

### MAST-Data
- 1,600+ annotated traces from 7 MAS frameworks
- First dataset capturing failure dynamics in multi-agent systems

### MAST Taxonomy (14 failure modes, 3 clusters)
1. **System design issues** — Flaws in how the MAS is architected
2. **Inter-agent misalignment** — Agents working at cross-purposes
3. **Task verification failures** — Inability to verify task completion

### LLM-as-a-Judge Pipeline
- Scalable annotation method using LLMs
- High agreement with human annotations (Cohen's kappa = 0.88)

## Key Findings
- MAS performance gains on benchmarks are often minimal
- Failures are systemic and classifiable — not random
- Better MAS design can significantly improve outcomes

## Relevance to Sub-Agent Delegation
Critical diagnostic framework for understanding why [[sub-agent]] coordination fails. When building pipelines with [[delegate_task]], the MAST taxonomy helps identify:
- System design issues (e.g., unclear task boundaries)
- Inter-agent misalignment (e.g., conflicting goals)
- Verification failures (e.g., no acceptance criteria)

## Cross-References
- [[sub-agent]] — Sub-agent patterns
- [[parallel-execution]] — Parallel execution risks
- [[context-isolation]] — Isolation as a design response
