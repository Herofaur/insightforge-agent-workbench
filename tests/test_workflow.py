import unittest

from insightforge.agents import extract_keywords, slugify
from insightforge.models import Requirement
from insightforge.orchestrator import run_workflow


class WorkflowTest(unittest.TestCase):
    def test_workflow_runs_all_agents(self) -> None:
        requirement = Requirement(
            title="AI Agent Delivery",
            body="Use AI agent collaboration to create a tested GitHub delivery plan.",
            tags=("agent", "github"),
        )

        report = run_workflow(requirement)

        self.assertEqual(
            [result.agent for result in report.results],
            [
                "Context Agent",
                "Planner Agent",
                "Coding Agent",
                "Test Agent",
                "Documentation Agent",
            ],
        )
        self.assertIn("AI 输出需要人工确认", "\n".join(report.by_agent("Context Agent").items))

    def test_report_markdown_contains_delivery_sections(self) -> None:
        requirement = Requirement(title="Import Flow", body="Build import workflow with validation.")

        markdown = run_workflow(requirement).to_markdown()

        self.assertIn("# InsightForge Report: Import Flow", markdown)
        self.assertIn("## Planner Agent", markdown)
        self.assertIn("## Test Agent", markdown)
        self.assertIn("覆盖成功路径和空输入", markdown)

    def test_keyword_extraction_and_slug_are_stable(self) -> None:
        self.assertEqual(
            extract_keywords("Build GitHub agent workflow, build tests")[:3],
            ("Build", "GitHub", "agent"),
        )
        self.assertEqual(slugify("AI Agent Delivery Plan!"), "ai-agent-delivery-plan")


if __name__ == "__main__":
    unittest.main()
