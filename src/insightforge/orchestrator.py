from __future__ import annotations

from .agents import CodingAgent, ContextAgent, DocAgent, PlannerAgent, TestAgent
from .models import AgentResult, Requirement, WorkflowReport


DEFAULT_AGENTS = (
    ContextAgent(),
    PlannerAgent(),
    CodingAgent(),
    TestAgent(),
    DocAgent(),
)


def run_workflow(requirement: Requirement) -> WorkflowReport:
    report = WorkflowReport(requirement=requirement)
    history: list[AgentResult] = []

    for agent in DEFAULT_AGENTS:
        result = agent.run(requirement, tuple(history))
        report.add(result)
        history.append(result)

    return report
