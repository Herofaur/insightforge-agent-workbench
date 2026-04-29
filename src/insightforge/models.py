from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Iterable


@dataclass(frozen=True)
class Requirement:
    title: str
    body: str
    tags: tuple[str, ...] = ()

    @property
    def text(self) -> str:
        chunks = [self.title.strip(), self.body.strip(), " ".join(self.tags)]
        return "\n".join(chunk for chunk in chunks if chunk)


@dataclass(frozen=True)
class AgentResult:
    agent: str
    summary: str
    items: tuple[str, ...] = ()


@dataclass
class WorkflowReport:
    requirement: Requirement
    results: list[AgentResult] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def add(self, result: AgentResult) -> None:
        self.results.append(result)

    def by_agent(self, agent: str) -> AgentResult:
        for result in self.results:
            if result.agent == agent:
                return result
        raise KeyError(f"Missing agent result: {agent}")

    def to_markdown(self) -> str:
        lines = [
            f"# InsightForge Report: {self.requirement.title}",
            "",
            f"Generated at: {self.created_at.isoformat(timespec='seconds')}",
            "",
            "## Requirement",
            "",
            self.requirement.body.strip(),
            "",
        ]

        if self.requirement.tags:
            lines.extend(["Tags: " + ", ".join(self.requirement.tags), ""])

        for result in self.results:
            lines.extend([f"## {result.agent}", "", result.summary, ""])
            if result.items:
                lines.extend(f"- {item}" for item in result.items)
                lines.append("")

        return "\n".join(lines).strip() + "\n"


def unique_ordered(values: Iterable[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        clean = value.strip()
        if clean and clean.lower() not in seen:
            seen.add(clean.lower())
            output.append(clean)
    return tuple(output)
