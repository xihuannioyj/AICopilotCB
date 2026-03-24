# AICopilotCB

这个目录是从 LiveHome 仓库中抽离出来的一份 AI 协同方案副本，用于后续做独立化、通用化整理。

当前目标只有两个：

1. 提供一个不依赖 LiveHome 业务上下文的独立阅读入口。
2. 在不影响现有 LiveHome 协同使用的前提下，为后续通用化拆分准备目录和说明。

## 当前状态

- 已复制 AI 协同方案相关核心文件到这个目录下。
- 原 LiveHome 项目中的协同规则、Agent、Prompt、Hook 和守卫脚本没有被替换。
- 这里目前仍保留 LiveHome 来源痕迹，但已经补上独立入口说明和通用化拆分方案。

## 建议阅读顺序

1. 先看 docs/AI协同方案需求大纲索引.md，理解需求主题与阅读顺序。
2. 再看 .github/copilot-instructions.md、.github/agents/、.github/prompts/，了解当前控制面和执行面。
3. 需要继续抽离时，再按 core/、stacks/、projects/livehome/ 三层目录推进落盘。

## 目录说明

- .github/：当前复制过来的协同控制入口、Agent、Prompt 和 Hook。
- docs/：当前需求索引与详细 requirements 文档。
- scripts/：当前复制过来的守卫脚本。
- core/：后续沉淀项目无关的通用协同规则。
- stacks/：后续沉淀 Java、Python、Go、Flutter、Angular、小程序等技术栈适配规则。
- projects/livehome/：后续承接 LiveHome 的项目覆盖层规则。

## 抽离原则

- 先复制，再整理，不直接替换原 LiveHome 协同文件。
- 先抽通用核心，再抽技术栈适配，最后保留项目覆盖。
- 任何仍然强依赖 LiveHome 的规则，都先留在项目覆盖层，不提前硬拆。

## 下一步建议

- 梳理 .github/copilot-instructions.md 中哪些规则属于通用核心。
- 把现有 Agent 的项目无关职责抽到 core/ 或 stacks/。
- 把 LiveHome 专属约束集中沉淀到 projects/livehome/。
