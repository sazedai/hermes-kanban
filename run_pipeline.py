#!/usr/bin/env python3
"""
run_pipeline.py — Execute a Hermes Kanban pipeline using sub-agent delegation.

This is the main entry point. It:
1. Parses the pipeline markdown
2. Creates a shared workspace for inter-agent file passing
3. Spawns sub-agents via delegate_task for each task (respecting dependencies)
4. Monitors progress and reports results

Usage:
    python3 run_pipeline.py pipelines/marketing.md [--workspace /path/to/workspace]
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime


# ── Pipeline Parser (same as orchestrator.py) ─────────────────────────────────

@dataclass
class Task:
    id: str = ""
    title: str = ""
    assignee: str = ""
    depends_on: list = field(default_factory=list)
    description: str = ""
    output: str = ""
    acceptance_criteria: list = field(default_factory=list)


def parse_pipeline(filepath: str) -> list[Task]:
    content = Path(filepath).read_text()
    tasks = []
    blocks = re.split(r'\n## Task \d+', content)
    blocks = blocks[1:] if len(blocks) > 1 else blocks

    for i, block in enumerate(blocks, 1):
        task = Task(id=f"T{i}")

        m = re.search(r'\*\*Title:\*\*\s*(.+?)(?:\n|$)', block)
        if m: task.title = m.group(1).strip()

        m = re.search(r'\*\*Assignee:\*\*\s*(.+?)(?:\n|$)', block)
        if m: task.assignee = m.group(1).strip()

        m = re.search(r'\*\*Depends On:\*\*\s*(.+?)(?:\n|$)', block)
        if m:
            dep_str = m.group(1).strip()
            if dep_str.lower() not in ('none', 'n/a', ''):
                for dep in re.split(r'[,;]', dep_str):
                    num = re.search(r'(\d+)', dep.strip())
                    if num:
                        task.depends_on.append(f"T{num.group(1)}")

        m = re.search(r'\*\*Description:\*\*\s*(.+?)(?=\n\*\*|$)', block, re.DOTALL)
        if m: task.description = m.group(1).strip()

        m = re.search(r'\*\*Output:\*\*\s*(.+?)(?=\n\*\*|$)', block)
        if m: task.output = m.group(1).strip()

        criteria = re.search(r'\*\*Acceptance Criteria:\*\*\s*\n((?:- .+\n?)+)', block)
        if criteria:
            for line in criteria.group(1).strip().split('\n'):
                line = line.strip().lstrip('- ').strip()
                if line:
                    task.acceptance_criteria.append(line)

        tasks.append(task)
    return tasks


# ── Agent Prompt Builder ──────────────────────────────────────────────────────

def load_soul(agent_role: str) -> str:
    """Load the soul file for an agent role."""
    soul_path = Path(__file__).parent / "soul" / f"{agent_role}.md"
    if soul_path.exists():
        return soul_path.read_text()
    return f"# Soul: {agent_role}\n\nYou are a {agent_role}."


def build_agent_prompt(task: Task, workspace: str, pipeline_name: str,
                       dependency_outputs: dict = None) -> str:
    """Build the full prompt for a sub-agent."""
    soul = load_soul(task.assignee)

    dep_context = ""
    if dependency_outputs:
        dep_context = "\n\n## Dependency Outputs\n"
        dep_context += "The following outputs from upstream tasks are available:\n\n"
        for dep_id, output in dependency_outputs.items():
            dep_file = Path(workspace) / f"{dep_id}_output.md"
            dep_context += f"- **{dep_id}**: Written to `{dep_file}`\n"
        dep_context += "\nRead these files before starting your work."

    acceptance = "\n".join(f"- {c}" for c in task.acceptance_criteria)

    prompt = f"""# Pipeline Task: {task.title}

## Your Role
{soul}

## Pipeline Context
Pipeline: {pipeline_name}
Task ID: {task.id}
Workspace: {workspace}

## Task
{task.description}

## Expected Output
{task.output}

## Acceptance Criteria
{acceptance}
{dep_context}

## Instructions
1. Read any dependency output files listed above
2. Execute the task according to your role's guidelines
3. Write your output to: `{workspace}/{task.id}_output.md`
4. Write a handoff summary to: `{workspace}/{task.id}_handoff.json`
5. The handoff JSON must include: {{"task_id": "{task.id}", "status": "complete", "summary": "...", "output_file": "{task.id}_output.md", "metadata": {{...}}}}

## Important
- Write ALL output files to the workspace: {workspace}
- Be specific and concrete — no filler
- Cite sources for all claims
- Follow your soul file's quality bar exactly
"""
    return prompt


# ── Pipeline Runner ───────────────────────────────────────────────────────────

def get_execution_levels(tasks: list[Task]) -> list[list[Task]]:
    """Group tasks into levels based on dependencies."""
    task_map = {t.id: t for t in tasks}
    levels = []
    completed = set()
    remaining = list(tasks)

    while remaining:
        level = [t for t in remaining if all(d in completed for d in t.depends_on)]
        if not level:
            print(f"ERROR: Circular dependency detected among: {[t.id for t in remaining]}")
            break
        levels.append(level)
        for t in level:
            completed.add(t.id)
            remaining.remove(t)

    return levels


def print_pipeline_summary(tasks: list[Task], levels: list[list[Task]]):
    """Print the pipeline execution plan."""
    print("\n" + "=" * 60)
    print("  PIPELINE EXECUTION PLAN")
    print("=" * 60)
    for i, level in enumerate(levels):
        print(f"\n  Level {i} (parallel):")
        for task in level:
            deps = ", ".join(task.depends_on) if task.depends_on else "None"
            print(f"    {task.id}: {task.title} [{task.assignee}] (deps: {deps})")
    print(f"\n  Total: {len(tasks)} tasks, {len(levels)} levels")
    print("=" * 60)


def generate_delegate_commands(tasks: list[Task], levels: list[list[Task]],
                                workspace: str, pipeline_name: str) -> str:
    """Generate the Python code that the orchestrator agent will execute."""
    lines = [
        "#!/usr/bin/env python3",
        '"""Auto-generated pipeline execution script.',
        'Run this inside a Hermes Agent session to execute the pipeline.',
        '"""',
        "",
        "import os",
        "import json",
        "from pathlib import Path",
        "",
        f'WORKSPACE = "{workspace}"',
        f'PIPELINE = "{pipeline_name}"',
        "RESULTS = {}",
        "",
        "def read_dep_outputs(task_id, dep_ids):",
        "    outputs = {}",
        "    for dep_id in dep_ids:",
        "        f = Path(WORKSPACE) / f'{dep_id}_output.md'",
        "        if f.exists():",
        "            outputs[dep_id] = f.read_text()",
        "    return outputs",
        "",
    ]

    for level_idx, level in enumerate(levels):
        lines.append(f"\n# ── Level {level_idx} ──")

        for task in level:
            soul = load_soul(task.assignee)
            prompt = build_agent_prompt(task, workspace, pipeline_name)

            # Escape the prompt for embedding
            prompt_escaped = prompt.replace('\\', '\\\\').replace('"""', '\\"\\"\\"')

            lines.append(f"\n# {task.id}: {task.title}")
            lines.append(f"print(f'\\n>>> Spawning {task.id}: {task.title}')")

            if task.depends_on:
                dep_list = ", ".join(f'"{d}"' for d in task.depends_on)
                lines.append(f"deps = read_dep_outputs('{task.id}', [{dep_list}])")
                lines.append(f"dep_context = '\\n'.join(f'{{k}}: {{v[:200]}}...' for k,v in deps.items())")
            else:
                lines.append("deps = {}")
                lines.append("dep_context = 'None'")

            lines.append(f"RESULTS['{task.id}'] = delegate_task(")
            lines.append(f'    goal="""{prompt_escaped}""",')
            lines.append(f"    role='leaf',")
            lines.append(f"    toolsets=['web', 'file'],")
            lines.append(f")")
            lines.append(f"print(f'  {task.id} result: {{RESULTS[\"{task.id}\"]}}')")

    lines.append("\n# ── Summary ──")
    lines.append("print('\\n=== PIPELINE COMPLETE ===')")
    lines.append("for tid, result in RESULTS.items():")
    lines.append("    print(f'  {tid}: {result.get(\"status\", \"?\")} - {result.get(\"summary\", \"\")[:100]}')")

    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Run a Hermes Kanban pipeline")
    parser.add_argument("pipeline", help="Path to pipeline markdown file")
    parser.add_argument("--workspace", default=None, help="Workspace directory")
    parser.add_argument("--dry-run", action="store_true", help="Show plan only")
    parser.add_argument("--generate", action="store_true", help="Generate execution script")
    args = parser.parse_args()

    # Parse
    tasks = parse_pipeline(args.pipeline)
    if not tasks:
        print("ERROR: No tasks found")
        sys.exit(1)

    levels = get_execution_levels(tasks)
    pipeline_name = Path(args.pipeline).stem

    # Workspace
    if args.workspace:
        workspace = args.workspace
    else:
        workspace = str(Path.home() / "hermes-kanban" / "workspaces" / f"{pipeline_name}-{datetime.now():%Y%m%d-%H%M%S}")

    Path(workspace).mkdir(parents=True, exist_ok=True)

    # Summary
    print_pipeline_summary(tasks, levels)
    print(f"\n  Workspace: {workspace}")
    print(f"  Tasks: {len(tasks)} | Levels: {len(levels)}")

    if args.generate:
        script = generate_delegate_commands(tasks, levels, workspace, pipeline_name)
        script_path = Path(workspace) / "execute.py"
        script_path.write_text(script)
        print(f"\n  Execution script: {script_path}")
        print("  Run inside Hermes Agent to execute the pipeline.")
        return

    if args.dry_run:
        print("\n  Dry run — no tasks executed.")
        print("  Use --generate to create the execution script.")
        return

    # Print the delegate_task commands for manual execution
    print("\n" + "=" * 60)
    print("  EXECUTION COMMANDS")
    print("=" * 60)
    print("\nCopy and run these inside your Hermes Agent session:\n")

    for level_idx, level in enumerate(levels):
        print(f"\n# Level {level_idx}:")
        for task in level:
            prompt = build_agent_prompt(task, workspace, pipeline_name)
            print(f"\n# --- {task.id}: {task.title} ---")
            print(f"delegate_task(")
            print(f'    goal="""{prompt}""",')
            print(f"    role='leaf',")
            print(f"    toolsets=['web', 'file'],")
            print(f")")

    print(f"\n\nWorkspace: {workspace}")
    print("All outputs will be written to the workspace directory.")


if __name__ == "__main__":
    main()
