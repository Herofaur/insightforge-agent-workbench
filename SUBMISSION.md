# Agent / AI Driven Achievement

我构建了一个名为 **InsightForge** 的多 Agent 智能研发工作台，用 AI 工作流把“需求理解、方案拆解、实现建议、测试验证、文档沉淀”串成闭环。项目要解决的核心痛点是：传统开发中需求容易散落在聊天记录、会议纪要和 issue 里，工程师需要反复理解上下文，测试与文档也常常滞后，导致交付效率低、返工率高。

系统采用“指挥官式编排器 + 专家 Agent”协作架构：Context Agent 负责提取关键词和潜在风险；Planner Agent 拆解任务并给出验收路径；Coding Agent 根据需求生成最小改动建议；Test Agent 自动整理边界用例；Documentation Agent 将最终决策沉淀为 GitHub 可读的交付说明。多个 Agent 之间通过共享报告同步信息，避免重复工作，并让每一步都可追溯、可评审。

最终产出包括一个可运行的 Python CLI、多 Agent 工作流源码、示例需求、单元测试、README 和 GitHub Actions 自动验证配置。运行 `insightforge --demo` 后，系统会生成一份完整的工程交付报告。它不是简单“让 AI 写代码”，而是把 AI 变成一个会规划、会协作、会自检的研发伙伴。
