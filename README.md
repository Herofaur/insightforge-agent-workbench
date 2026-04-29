# InsightForge Agent Workbench

InsightForge is a local multi-agent workflow prototype that turns a product requirement into a delivery-ready engineering report.

It does not call any external AI service. Instead, it demonstrates the architecture behind an Agent-driven development loop: context discovery, task planning, implementation guidance, test design, and documentation handoff.

## Why It Exists

Modern teams often lose time because requirements live across chats, meetings, issues, and partial documents. InsightForge gives that scattered input a simple structure:

- **Context Agent** extracts keywords, risks, and shared background.
- **Planner Agent** breaks the work into verifiable steps.
- **Coding Agent** suggests a review-friendly implementation direction.
- **Test Agent** turns risk into a focused test checklist.
- **Documentation Agent** prepares the handoff material for GitHub.

The goal is not to replace engineers. The goal is to make the first pass of engineering thinking visible, reviewable, and repeatable.

## Quick Start

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -e .
insightforge --demo
```

On macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
insightforge --demo
```

## Use Your Own Requirement

```bash
insightforge --title "Payment Retry Flow" --file examples/payment-retry.txt --tag payment --tag reliability
```

Write the result to a Markdown file:

```bash
insightforge --demo --output reports/demo-report.md
```

## Example Output

The generated report includes:

- a requirement summary
- one section per Agent
- implementation suggestions
- test checklist
- documentation notes

That makes it suitable for PR descriptions, issue planning, hackathon submissions, or portfolio demos.

## Project Structure

```text
insightforge-agent-workbench/
  src/insightforge/
    agents.py          # Local Agent implementations
    orchestrator.py    # Workflow runner
    models.py          # Dataclasses and report model
    cli.py             # Command-line interface
  tests/
    test_workflow.py
  examples/
    payment-retry.txt
```

## Development

```bash
pip install -e .
python -m unittest discover -s tests
```

## Creative Submission Summary

InsightForge packages Agent collaboration into a small, understandable engineering workflow. It shows how AI-assisted development can be more than code generation: the system plans, checks risk, proposes implementation boundaries, creates tests, and writes the delivery notes needed for a GitHub review.

## License

MIT
