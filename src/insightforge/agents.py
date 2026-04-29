from __future__ import annotations

import re
from dataclasses import dataclass

from .models import AgentResult, Requirement, unique_ordered


RISK_WORDS = {
    "auth": "认证或权限边界需要额外验证",
    "login": "登录流程可能影响核心转化路径",
    "payment": "支付链路需要回归失败和幂等场景",
    "delete": "删除操作需要确认恢复或审计策略",
    "performance": "性能目标需要可量化基线",
    "import": "导入流程需要处理脏数据和重复数据",
    "export": "导出结果需要验证格式和权限",
    "ai": "AI 输出需要人工确认和可追溯记录",
    "agent": "Agent 协作需要状态同步和失败恢复",
}


@dataclass(frozen=True)
class BaseAgent:
    name: str

    def run(self, requirement: Requirement, previous: tuple[AgentResult, ...]) -> AgentResult:
        raise NotImplementedError


class ContextAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__("Context Agent")

    def run(self, requirement: Requirement, previous: tuple[AgentResult, ...]) -> AgentResult:
        keywords = extract_keywords(requirement.text)
        risks = [
            message
            for word, message in RISK_WORDS.items()
            if re.search(rf"\b{re.escape(word)}\b", requirement.text, flags=re.I)
        ]
        items = unique_ordered((*keywords[:6], *risks[:3]))
        summary = "识别需求背景、关键词和潜在风险，为后续 Agent 提供共享上下文。"
        return AgentResult(self.name, summary, items)


class PlannerAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__("Planner Agent")

    def run(self, requirement: Requirement, previous: tuple[AgentResult, ...]) -> AgentResult:
        context = previous[-1].items if previous else ()
        items = [
            "澄清输入、输出和验收标准",
            "定位受影响模块并保持最小改动",
            "实现核心路径并补充边界处理",
            "运行自动化测试并生成交付摘要",
        ]
        if any("AI" in item or "Agent" in item for item in context):
            items.insert(2, "记录 Agent 决策链，保留人工确认节点")
        summary = "将需求拆成可执行步骤，并明确每一步的验证方式。"
        return AgentResult(self.name, summary, tuple(items))


class CodingAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__("Coding Agent")

    def run(self, requirement: Requirement, previous: tuple[AgentResult, ...]) -> AgentResult:
        title_slug = slugify(requirement.title)
        items = (
            f"新增或更新 feature/{title_slug} 相关入口",
            "复用现有模型和工具函数，避免一次性抽象",
            "把不可确定的外部行为封装在清晰接口后",
            "保持补丁可评审：小函数、明确命名、无无关格式化",
        )
        summary = "生成面向代码评审的实现建议，而不是直接扩大功能范围。"
        return AgentResult(self.name, summary, items)


class TestAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__("Test Agent")

    def run(self, requirement: Requirement, previous: tuple[AgentResult, ...]) -> AgentResult:
        text = requirement.text.lower()
        items = [
            "覆盖成功路径和空输入",
            "覆盖无效输入、重复提交和异常分支",
            "验证输出结构稳定，便于后续自动化消费",
        ]
        if "performance" in text or "性能" in text:
            items.append("记录性能基线，避免优化结果不可复现")
        if "permission" in text or "auth" in text or "权限" in text:
            items.append("增加越权访问和未登录访问用例")
        summary = "把需求转成可运行的测试清单，降低遗漏风险。"
        return AgentResult(self.name, summary, tuple(items))


class DocAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__("Documentation Agent")

    def run(self, requirement: Requirement, previous: tuple[AgentResult, ...]) -> AgentResult:
        items = (
            "README 中说明使用场景、安装方式和运行命令",
            "CHANGELOG 中记录用户可感知变化",
            "PR 描述中附上风险、测试结果和回滚方式",
        )
        summary = "沉淀交付资料，让代码之外的决策也能被追踪。"
        return AgentResult(self.name, summary, items)


def extract_keywords(text: str) -> tuple[str, ...]:
    words = re.findall(r"[A-Za-z][A-Za-z0-9_-]{2,}|[\u4e00-\u9fff]{2,}", text)
    stop_words = {"the", "and", "for", "with", "this", "that", "from", "into", "需求", "项目"}
    return unique_ordered(word for word in words if word.lower() not in stop_words)


def slugify(value: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+|[\u4e00-\u9fff]+", value.lower())
    if not words:
        return "new-workflow"
    return "-".join(words[:6])
