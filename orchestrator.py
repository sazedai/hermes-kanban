#!/usr/bin/env python3
"""
orchestrator.py — Hermes Kanban Pipeline Orchestrator

Reads a markdown pipeline definition, parses the task graph, and creates
kanban tasks with proper dependency links using the Hermes kanban_* tools.

Usage:
    python3 orchestrator.py <pipeline.md> [--dry-run] [--board <name>]

The orchestrator expects to be run inside a Hermes Agent context where
the kanban_* tools are available. For standalone testing, use --dry-run.
"""

import re
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    id: str = ""
    title: str = ""
    assignee: str = ""
    depends_on: list = field(default_factory=list)
    description: str = ""
    output: str = ""
    acceptance_criteria: list = field(default_factory=list)
    raw: str = ""


def parse_pipeline(filepath: str) -> list[Task]:
    """Parse a markdown pipeline file into a list of Task objects."""
    content = Path(filepath).read_text()
    tasks = []

    # Split into task blocks by "## Task N"
    blocks = re.split(r'\n## Task \d+', content)
    # First block is the header/preamble, skip it
    blocks = blocks[1:] if len(blocks) > 1 else blocks

    for i, block in enumerate(blocks, 1):
        task = Task(id=f"T{i}", raw=block.strip())

        # Parse fields
        title_match = re.search(r'\*\*Title:\*\*\s*(.+?)(?:\n|$)', block)
        if title_match:
            task.title = title_match.group(1).strip()

        assignee_match = re.search(r'\*\*Assignee:\*\*\s*(.+?)(?:\n|$)', block)
        if assignee_match:
            task.assignee = assignee_match.group(1).strip()

        depends_match = re.search(r'\*\*Depends On:\*\*\s*(.+?)(?:\n|$)', block)
        if depends_match:
            depends_str = depends_match.group(1).strip()
            if depends_str.lower() not in ('none', 'n/a', ''):
                # Parse "Task 1, Task 2" or "T1, T2" format
                for dep in re.split(r'[,;]', depends_str):
                    dep = dep.strip()
                    # Normalize to T{N} format
                    num = re.search(r'(\d+)', dep)
                    if num:
                        task.depends_on.append(f"T{num.group(1)}")

        desc_match = re.search(r'\*\*Description:\*\*\s*(.+?)(?=\n\*\*|$)', block, re.DOTALL)
        if desc_match:
            task.description = desc_match.group(1).strip()

        output_match = re.search(r'\*\*Output:\*\*\s*(.+?)(?:\n\*\*|$)', block)
        if output_match:
            task.output = output_match.group(1).strip()

        # Parse acceptance criteria
        criteria_section = re.search(r'\*\*Acceptance Criteria:\*\*\s*\n((?:- .+\n?)+)', block)
        if criteria_section:
            for line in criteria_section.group(1).strip().split('\n'):
                line = line.strip().lstrip('- ').strip()
                if line:
                    task.acceptance_criteria.append(line)

        tasks.append(task)

    return tasks


def validate_graph(tasks: list[Task]) -> list[str]:
    """Validate the task graph for cycles and missing dependencies."""
    errors = []
    task_ids = {t.id for t in tasks}

    for task in tasks:
        for dep in task.depends_on:
            if dep not in task_ids:
                errors.append(f"  {task.id}: depends on {dep} which doesn't exist")

    # Check for cycles (simple DFS)
    visited = set()
    rec_stack = set()

    def has_cycle(task_id, adj):
        visited.add(task_id)
        rec_stack.add(task_id)
        for neighbor in adj.get(task_id, []):
            if neighbor not in visited:
                if has_cycle(neighbor, adj):
                    return True
            elif neighbor in rec_stack:
                return True
        rec_stack.discard(task_id)
        return False

    adj = {t.id: t.depends_on for t in tasks}
    for t in tasks:
        if t.id not in visited:
            if has_cycle(t.id, adj):
                errors.append(f"  Cycle detected involving {t.id}")

    return errors


def print_graph(tasks: list[Task]):
    """Print the task dependency graph."""
    print("\nTask Dependency Graph:")
    print("=" * 60)

    # Group by level (topological levels)
    levels = {}
    for task in tasks:
        if not task.depends_on:
            levels.setdefault(0, []).append(task)
        else:
            max_parent_level = max(
                next((l for l, ts in levels.items() if any(t.id == dep for t in ts)), -1)
                for dep in task.depends_on
            )
            levels.setdefault(max_parent_level + 1, []).append(task)

    for level, level_tasks in sorted(levels.items()):
        print(f"\n  Level {level}:")
        for task in level_tasks:
            deps = ", ".join(task.depends_on) if task.depends_on else "None"
            print(f"    {task.id}: {task.title}")
            print(f"       Assignee: {task.assignee} | Depends on: {deps}")

    print(f"\n  Total: {len(tasks)} tasks, {len(levels)} levels")
    print("=" * 60)


def generate_kanban_commands(tasks: list[Task], board_name: str = "pipeline") -> str:
    """Generate Python code that creates kanban tasks with proper links."""
    lines = [
        "#!/usr/bin/env python3",
        "# Auto-generated kanban creation script",
        "# Run this inside a Hermes Agent session",
        "",
        "import os",
        "",
        f'BOARD = "{board_name}"',
        "TASK_IDS = {}",
        "",
        "# Phase 1: Create independent tasks (no parents)",
    ]

    # Create tasks level by level
    created = set()
    remaining = list(tasks)
    phase = 1

    while remaining:
        batch = [t for t in remaining if all(d in created for d in t.depends_on)]
        if not batch:
            lines.append(f"\n# ERROR: Circular dependency detected")
            break

        lines.append(f"\n# Phase {phase}: Create batch")
        for task in batch:
            title = task.title.replace('"', '\\"')
            desc = task.description.replace('"', '\\"').replace('\n', '\\n')
            criteria = "\\n".join(task.acceptance_criteria)

            parents_arg = ""
            if task.depends_on:
                parent_ids = ", ".join(f'TASK_IDS["{d}"]' for d in task.depends_on)
                parents_arg = f", parents=[{parent_ids}]"

            lines.append(f'TASK_IDS["{task.id}"] = kanban_create(')
            lines.append(f'    title="{title}",')
            lines.append(f'    assignee="{task.assignee}",')
            lines.append(f'    body="""{desc}')
            lines.append(f'')
            lines.append(f'Acceptance Criteria:')
            lines.append(f'{criteria}""",')
            lines.append(f'    tenant=os.environ.get("HERMES_TENANT"),')
            lines.append(f')["task_id"]')
            lines.append(f'print(f"  Created {task.id}: {{TASK_IDS[\"{task.id}\"]}}")')

            created.add(task.id)
            remaining.remove(task)

        phase += 1

    lines.append(f'\nprint(f"\\nAll {len(tasks)} tasks created.")')
    lines.append('print("Use `hermes kanban list` to view the board.")')

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Hermes Kanban Pipeline Orchestrator")
    parser.add_argument("pipeline", help="Path to pipeline markdown file")
    parser.add_argument("--dry-run", action="store_true", help="Parse and validate only, don't create tasks")
    parser.add_argument("--board", default="pipeline", help="Board/tenant name")
    parser.add_argument("--generate", action="store_true", help="Generate kanban creation script")
    args = parser.parse_args()

    # Parse
    print(f"Parsing pipeline: {args.pipeline}")
    tasks = parse_pipeline(args.pipeline)

    if not tasks:
        print("ERROR: No tasks found in pipeline file")
        sys.exit(1)

    print(f"Found {len(tasks)} tasks")

    # Validate
    errors = validate_graph(tasks)
    if errors:
        print("\nValidation errors:")
        for e in errors:
            print(e)
        sys.exit(1)

    print("Graph validation: PASS")

    # Print graph
    print_graph(tasks)

    if args.generate:
        script = generate_kanban_commands(tasks, args.board)
        out_path = Path(args.pipeline).stem + "-kanban.py"
        Path(out_path).write_text(script)
        print(f"\nKanban creation script written to: {out_path}")
        print(f"Run inside Hermes Agent to create tasks.")
        return

    if args.dry_run:
        print("\nDry run — no tasks created.")
        print("Run without --dry-run to create kanban tasks.")
        return

    # Generate the creation script for the user
    print("\nTo create these tasks in Hermes Kanban:")
    print(f"  python3 {__file__} {args.pipeline} --generate")
    print("Then run the generated script inside a Hermes Agent session.")


if __name__ == "__main__":
    main()
