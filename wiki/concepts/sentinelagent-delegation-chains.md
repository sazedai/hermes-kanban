---
title: SentinelAgent: Verifiable Delegation Chains
created: 2026-06-05
updated: 2026-06-05
type: concept
tags: [delegation, sub-agent, agent, orchestration, workflow]
sources: [raw/papers/2604.02767.md]
confidence: high
---

# SentinelAgent: Verifiable Delegation Chains

## Summary

"SentinelAgent: Intent-Verified Delegation Chains for Securing Federal Multi-Agent AI Systems" (arXiv:2604.02767, Apr 2026) by KrishnaSaiReddy Patil introduces a **formal security framework for delegation chains** in multi-agent systems. The core problem: when Agent A delegates to Agent B which invokes Tool C on behalf of User X, no existing framework can trace the authorization chain or detect policy violations.

The paper introduces the **Delegation Chain Calculus (DCC)** with seven formal properties, the **Intent-Preserving Delegation Protocol (IPDP)** for runtime enforcement, and a **Delegation Authority Service (DAS)** that achieves 100% true positive rate at 0% false positive rate on security benchmarks.

## Key Techniques / Methods

### Delegation Chain Calculus (DCC)
Seven formal properties governing secure delegation:
1. **Authority narrowing** — Delegated authority must not exceed the delegator's scope
2. **Policy preservation** — All policies must be maintained through the chain
3. **Forensic reconstructibility** — Full audit trail of delegation decisions
4. **Cascade containment** — Delegation chains must be bounded and traceable
5. **Scope-action conformance** — Actions must match the granted scope
6. **Output schema conformance** — Outputs must conform to expected schemas
7. **Intent preservation** — The original intent must be maintained (probabilistic)

### Intent-Preserving Delegation Protocol (IPDP)
- Runtime enforcement of all seven DCC properties
- Non-LLM Delegation Authority Service (DAS) for deterministic verification
- Three-point verification lifecycle: pre-delegation, runtime, post-execution

### Formal Verification
- TLA+ model checking across **2.7 million states** with zero violations
- Four meta-theorems and one proposition on the limits of deterministic intent verification
- DelegationBench v4 benchmark: 516 scenarios, 10 attack categories, 13 federal domains

## Relevance to AI Agent Delegation

This paper provides the **security and verification backbone** for production agent delegation systems. Key implications:

- **Sub-agent authorization** can be formally verified, not just heuristically trusted
- **Audit trails** are built into the delegation protocol itself
- **Adversarial robustness** is measurable and enforceable
- The framework demonstrates that even when intent verification is evaded, the remaining six properties constrain adversaries to permitted behaviors

This is essential reading for anyone building [[sub-agent-delegation-patterns]] in security-sensitive contexts.

## Cross-References
- [[intelligent-ai-delegation]] — The broader adaptive delegation framework
- [[context-isolation]] — Scope-action conformance relates to context boundaries
- [[multi-agent-orchestration]] — Enterprise orchestration needs these security properties
- [[context-engineering]] — Intent preservation connects to intent engineering
