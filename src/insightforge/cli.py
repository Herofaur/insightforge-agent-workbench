from __future__ import annotations

import argparse
from pathlib import Path

from .models import Requirement
from .orchestrator import run_workflow


DEMO_REQUIREMENT = """Build an AI agent workbench that turns scattered product notes into a delivery-ready engineering plan.
The workflow should identify context, split tasks, suggest implementation direction, create a test checklist,
and produce documentation notes for a GitHub pull request."""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="insightforge",
        description="Run a local multi-agent workflow over a product requirement.",
    )
    parser.add_argument("--title", default="Agent Workbench", help="Requirement title.")
    parser.add_argument("--text", help="Requirement body. If omitted, --file or --demo is used.")
    parser.add_argument("--file", type=Path, help="Read requirement body from a text file.")
    parser.add_argument("--tag", action="append", default=[], help="Add a requirement tag. Can be repeated.")
    parser.add_argument("--output", type=Path, help="Write the markdown report to this path.")
    parser.add_argument("--demo", action="store_true", help="Run with the bundled demo requirement.")
    args = parser.parse_args(argv)

    body = resolve_body(args.text, args.file, args.demo)
    requirement = Requirement(title=args.title, body=body, tags=tuple(args.tag))
    report = run_workflow(requirement)
    markdown = report.to_markdown()

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(markdown, encoding="utf-8")
    else:
        print(markdown, end="")

    return 0


def resolve_body(text: str | None, file: Path | None, demo: bool) -> str:
    if text:
        return text
    if file:
        return file.read_text(encoding="utf-8").strip()
    if demo:
        return DEMO_REQUIREMENT
    raise SystemExit("Please provide --text, --file, or --demo.")


if __name__ == "__main__":
    raise SystemExit(main())
