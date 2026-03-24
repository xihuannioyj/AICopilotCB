# AICopilotCB

AICopilotCB 是一个面向 AI 协作控制面的独立工程，用于持续沉淀、验证和演进 Agent、Prompt、Hook、守卫脚本、任务模板与协作规则。

## 当前目标

1. 把协同方案作为独立工程维护，而不是依附某个业务项目叙事。
2. 把通用核心、技术栈适配、项目覆盖和运行守卫拆成可复用、可裁剪、可持续演进的结构。
3. 为后续治理流程、自检能力和专属演进 Agent 提供稳定载体。

## 当前状态

- 仓库已具备协同控制面、需求文档、守卫脚本和任务模板骨架。
- 目录已经按 core/、stacks/、projects/ 分层，便于后续继续抽象和沉淀。
- docs/ 与 tasks/ 已补齐运行导航、Readiness 清单、人工主看板和 runtime 占位骨架。
- 当前重点是让控制面自身持续进化，而不是承载单一业务项目介绍。

## 建议阅读顺序

1. 先看 docs/AI协同方案需求大纲索引.md，理解需求主题与阅读顺序。
2. 再看 docs/AUTO_DEV_NAVIGATION.md 与 docs/初始化配置与运行时上下文说明.md，理解运行导航与配置真源。
3. 然后看 .github/copilot-instructions.md、.github/agents/、.github/prompts/，了解当前控制面和执行面。
4. 最后根据目标进入 core/、stacks/、projects/ 对应层继续扩展。

## 目录说明

- .github/：协同控制入口、Agent、Prompt、Hook 与 AUTO_DEV 配置。
- docs/：需求索引、运行导航、操作 Runbook、检查清单与汇报模板。
- tasks/：人工主看板、候选池、治理任务表、runtime 主数据与业务模板。
- scripts/：守卫脚本与 AUTO_DEV 占位脚本入口。
- core/：项目无关、技术栈无关的通用协同规则。
- stacks/：各技术栈适配规则与接入约束。
- projects/：具体项目覆盖层与兼容样例。

## 演进原则

- 先稳定协同底座，再扩展适配层和项目覆盖层。
- 优先沉淀可复用规则，避免把单项目例外误写成全局默认。
- 所有控制面变更都要保留机器可识别标记与守卫校验闭环。

## 下一步建议

- 继续收敛 .github/copilot-instructions.md 中的全局通用规则。
- 继续把新项目装配模板和第二项目验证路径固化下来。
- 补齐更多技术栈适配说明和项目覆盖模板。
