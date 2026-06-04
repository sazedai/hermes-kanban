#!/usr/bin/env python3
import hashlib

papers = {
    "2602.11865": """# Intelligent AI Delegation

**arXiv:2602.11865** | Submitted: 12 Feb 2026 | cs.AI

## Authors
- Nenad Tomašev
- Matija Franklin
- Simon Osindero

## Abstract

AI agents are able to tackle increasingly complex tasks. To achieve more ambitious goals, AI agents need to be able to meaningfully decompose problems into manageable sub-components, and safely delegate their completion across to other AI agents and humans alike. Yet, existing task decomposition and delegation methods rely on simple heuristics, and are not able to dynamically adapt to environmental changes and robustly handle unexpected failures. Here we propose an adaptive framework for intelligent AI delegation — a sequence of decisions involving task allocation, that also incorporates transfer of authority, responsibility, accountability, clear specifications regarding roles and boundaries, clarity of intent, and mechanisms for establishing trust between the two (or more) parties. The proposed framework is applicable to both human and AI delegators and delegatees in complex delegation networks, aiming to inform the development of protocols in the emerging agentic web.

## Key Problem
- Current AI task decomposition and delegation methods rely on simple heuristics
- They cannot dynamically adapt to environmental changes
- They fail to robustly handle unexpected failures

## Proposed Solution: Adaptive Framework for Intelligent AI Delegation
The paper introduces a framework for delegation as a sequence of decisions involving:
- Task allocation: Deciding which sub-tasks go to which agents
- Transfer of authority: Granting decision-making power to delegatees
- Responsibility: Defining who is answerable for outcomes
- Accountability: Ensuring traceability of actions and decisions
- Roles & boundaries: Clear specifications of scope and limits
- Clarity of intent: Explicit communication of goals and expectations
- Trust mechanisms: Establishing reliability between delegating parties

## Scope & Applicability
- Works for both human and AI delegators and delegatees
- Designed for complex delegation networks
- Aims to inform protocol development for the emerging agentic web""",

    "2604.02767": """# SentinelAgent: Intent-Verified Delegation Chains for Securing Federal Multi-Agent AI Systems

**arXiv:2604.02767** | Submitted: 3 Apr 2026 | cs.CR / cs.AI / cs.MA

## Authors
- KrishnaSaiReddy Patil

## Abstract

When Agent A delegates to Agent B, which invokes Tool C on behalf of User X, no existing framework can answer: whose authorization chain led to this action, and where did it violate policy? This paper introduces SentinelAgent, a formal framework for verifiable delegation chains in federal multi-agent AI systems. The Delegation Chain Calculus (DCC) defines seven properties - six deterministic (authority narrowing, policy preservation, forensic reconstructibility, cascade containment, scope-action conformance, output schema conformance) and one probabilistic (intent preservation) - with four meta-theorems and one proposition establishing the practical infeasibility of deterministic intent verification. The Intent-Preserving Delegation Protocol (IPDP) enforces all seven properties at runtime through a non-LLM Delegation Authority Service. A three-point verification lifecycle achieves 100% combined TPR at 0% FPR on DelegationBench v4 (516 scenarios, 10 attack categories, 13 federal domains). Under black-box adversarial conditions, the DAS blocks 30/30 attacks with 0 false positives. Deterministic properties are unbreakable under adversarial stress testing; intent verification degrades to 13% against sophisticated paraphrasing. Fine-tuning the NLI model on 190 government delegation examples improves P2 from 1.7% to 88.3% TPR (5-fold cross-validated, F1=82.1%). Properties P1, P3-P7 are mechanically verified via TLA+ model checking across 2.7 million states with zero violations. Even when intent verification is evaded, the remaining six properties constrain the adversary to permitted API calls, conformant outputs, traceable actions, bounded cascades, and compliant behavior.

## Key Contributions
- Delegation Chain Calculus (DCC) with 7 formal properties
- Intent-Preserving Delegation Protocol (IPDP) for runtime enforcement
- Delegation Authority Service (DAS) - non-LLM verification layer
- DelegationBench v4 benchmark (516 scenarios, 10 attack categories)
- TLA+ mechanical verification across 2.7 million states
- 100% TPR at 0% FPR on delegation security benchmarks""",

    "2601.13671": """# The Orchestration of Multi-Agent Systems: Architectures, Protocols, and Enterprise Adoption

**arXiv:2601.13671** | Published: January 20, 2026 | cs.MA / cs.AI

## Authors
- Apoorva Adimulam
- Rajesh Gupta
- Sumit Kumar

## Abstract

Orchestrated multi-agent systems represent the next stage in the evolution of artificial intelligence, where autonomous agents collaborate through structured coordination and communication to achieve complex, shared objectives. This paper consolidates and formalizes the technical composition of such systems, presenting a unified architectural framework that integrates planning, policy enforcement, state management, and quality operations into a coherent orchestration layer. Together, these protocols establish an interoperable communication substrate that enables scalable, auditable, and policy-compliant reasoning across distributed agent collectives.

## Core Contributions
- Unified architectural framework integrating planning, policy enforcement, state management, and quality operations
- Technical delineation of Model Context Protocol (MCP) for standardized tool/context access
- Agent2Agent Protocol (A2A) for peer coordination, negotiation, and delegation
- Enterprise adoption patterns with governance and observability mechanisms
- Implementation-ready design principles for scalable AI ecosystems

## Key Design Principles
- Structured coordination for complex, shared objectives
- Policy-compliant reasoning across distributed systems
- Interoperable communication substrate (MCP + A2A)
- Governance frameworks for transparency and accountability""",

    "2603.09619": """# Context Engineering: From Prompts to Corporate Multi-Agent Architecture

**arXiv:2603.09619** | Published: March 10, 2026 | cs.AI / cs.MA

## Authors
- Vera V. Vishnyakova

## Abstract

As AI systems evolve from stateless chatbots to autonomous multi-step agents, traditional prompt engineering (PE) becomes necessary but insufficient. The paper introduces Context Engineering (CE) as a standalone discipline focused on designing, structuring, and managing the entire informational environment in which an AI agent operates. Whoever controls the agent's context controls its behavior; whoever controls its intent controls its strategy; whoever controls its specifications controls its scale.

## Key Contributions
1. Context Engineering (CE): Managing the full informational environment for AI decision-making. Five context quality criteria: Relevance, Sufficiency, Isolation, Economy, Provenance
2. Intent Engineering (IE): Encoding organizational goals, values, and trade-off hierarchies into agent infrastructure
3. Specification Engineering (SE): Creating machine-readable corpus of corporate policies and standards for autonomous operation at scale
4. Agent Engineering Maturity Model: Cumulative pyramid of PE -> CE -> IE -> SE

## Key Insight
While 75% of enterprises plan agentic AI deployment within two years, deployment has surged and retreated as organizations confront scaling complexity. The layered maturity model addresses the gap between intent to deploy and ability to scale.""",

    "2603.15690": """# Loosely-Structured Software: Engineering Context, Structure, and Evolution Entropy in Runtime-Rewired Multi-Agent Systems

**arXiv:2603.15690** | Submitted: March 16, 2026 | cs.SE / cs.AI

## Authors
- Weihao Zhang
- Yitong Zhou
- Huanyu Qu
- Hongyi Li

## Abstract

As LLM-based multi-agent systems (MAS) become more autonomous, their free-form interactions increasingly dominate system behavior. However, scaling agents introduces context pressure, coordination errors, and system drift. Building robust MAS requires more than prompt tuning or increased model intelligence. It necessitates engineering discipline focused on architecture to manage complexity under uncertainty.

## Key Concept: Loosely-Structured Software (LSS)
A new class of software systems defined by runtime generation and evolution under uncertainty. LSS shifts engineering focus from constructing deterministic logic to managing runtime entropy generated by view-constructed programming, semantic-driven self-organization, and endogenous evolution.

## Three-Layer Engineering Framework
1. View/Context Engineering: Manage execution environment; maintain task-relevant Views
2. Structure Engineering: Organize dynamic binding over artifacts and agents
3. Evolution Engineering: Govern lifecycle of self-rewriting artifacts

## Outcomes
- Design patterns as semantic control blocks
- Stabilizes fluid, inference-mediated interactions while preserving agent adaptability
- Improves designability, scalability, and evolvability"""
}

for arxiv_id, body in papers.items():
    h = hashlib.sha256(body.encode('utf-8')).hexdigest()
    print(f"{arxiv_id}: {h}")
