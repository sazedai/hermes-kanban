---
title: Hermes Agent
created: 2026-06-05
updated: 2026-06-05
type: entity
tags: [agent, skills, profiles, workflow]
sources: []
confidence: medium
---

# Hermes Agent

Hermes Agent is an open-source AI assistant framework developed by [Nous Research](https://nousresearch.com). It operates as a CLI-first agent that can delegate tasks, manage sub-agents, execute code, and maintain persistent knowledge through a wiki system.

## Key Features

- **Sub-agent delegation** — spawn isolated [[sub-agent]]s via the [[delegate-task]] tool
- **Skill system** — modular capabilities loaded from the `skills/` directory
- **Profile isolation** — separate skills, plugins, cron, and memories per profile
- **Wiki integration** — persistent knowledge base with [[wikilinks]] and frontmatter
- **Goal mode** — autonomous execution until the stated objective is achieved ([[goal-mode]])
- **Tool access** — file read/write/edit, shell commands, Linear integration via MCP
- **Cron scheduling** — periodic tasks defined per profile

## Architecture

Hermes runs as a single-process CLI agent. When a task is delegated, it spawns a child sub-agent with its own context, instruction text, and identity. This enables [[context-isolation]] and [[parallel-execution]] profiles.

## Configuration

- Profiles live under `~/.hermes/profiles/<name>/`
- Each profile has its own: `skills/`, `plugins/`, `cron/`, `memories/`
- The active profile is set per session
- Skills are Markdown + YAML frontmatter files

## See Also

- [[sub-agent]] — the delegation model
- [[delegate-task]] — the tool used to spawn sub-agents
- [[parallel-execution]] — running multiple agents concurrently
- [[context-isolation]] — why sub-agents have independent context
