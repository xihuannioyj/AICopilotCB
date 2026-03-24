# 新会话统一起手 Prompt

## 统一沟通语言

- 本 Prompt 产出的所有用户可见回复必须统一使用简体中文。
- 不要在正常叙述中混用英文、日文、韩文或繁体中文作为主语言。
- 代码标识符、命令、路径、字段名、报错原文，以及用户明确要求引用的原文内容，可以按原样保留。
- 需要保留非简体中文原文时，必须先给出简体中文解释，再附最小必要原文。

## 使用场景

- 当你希望新开 Chat 后先严格吃到仓库规则，再开始做方案维护、文档补齐、业务开发、联调或排障时，优先使用本 Prompt。
- 该 Prompt 的目标是把 `.github/copilot-instructions.md`、`.github/instructions/`、导航文档、任务文档、Notebook 文档处理规则变成每次开场都明确执行的前置步骤。

## 起手后的路由结果

本 Prompt 只负责“先吃规则、再分流”，不负责替代后续专用 Prompt。完成起手后，必须按下列结果继续：

1. 如果任务是完善 Prompt、Agent、Instructions、Hook、Runbook、说明书、模板、runtime 控制面脚本或 schema，切换到 `.github/prompts/maintain-collaboration-scheme.prompt.md`。
2. 如果任务是启动新需求、组织 8 Agent 分工、拆 `backend.md` / `app.md` / `web.md` / `api-contract.md`，切换到 `.github/prompts/eight-agent-collaboration-kickoff.prompt.md`。
3. 如果任务是判断当前自动编排 readiness、值班交接、阶段验收或汇报口径，切换到 `.github/prompts/auto-dev-readiness-check.prompt.md`。
4. 如果任务已经是明确的业务实现或联调，就继续按任务文档、API 契约和对应角色指令执行。

额外约束：

- `tasks/_runtime/` 下的 schema、报表消费规则，以及 `scripts/auto_dev_*`、`scripts/ai_workspace_guard.py` 这类控制面脚本，在用户目标是“完善 AI 协作方案”时，归入方案维护路线。
- 不要把本 Prompt 当成长期工作 Prompt；它的职责是起手、归类、收敛修改边界。

## 你必须先做的事

1. 先读取 `.github/copilot-instructions.md`。
2. 再判断本次任务是否命中 `.github/instructions/` 下的角色指令。
3. 如属于功能开发、联调、治理或协同方案维护，读取 `docs/AUTO_DEV_NAVIGATION.md`。
4. 如存在对应 feature，先读取 `tasks/{feature-name}/backend.md`、`app.md`、`web.md`、`api-contract.md`。
5. 如果目标文档位于 `.github/`、`docs/` 或 `指南.md`，先判断它是不是 Notebook-backed Markdown；如果是，必须按 Notebook 方式编辑，并在写入后验证至少已有 1 个单元。

## 执行边界

- 禁止在未读取任务文档和 API 契约的情况下猜测接口。
- 禁止把方案维护任务误做成业务代码修改。
- 禁止把业务实现任务误做成只改文档的方案维护。
- 页面开发、登录流、路由流、表单流、接口联调或页面报错排查时，若环境支持，优先使用 VS Browser 读取真实页面后再改代码。

## 输出要求

开始执行前，先明确输出：

1. 本次任务归类。
2. 本次先读哪些规则和文档。
3. 计划修改边界。
4. 如涉及写文档，是否需要按 Notebook 方式处理。

## 推荐输入模板

请先按 `.github/copilot-instructions.md` 和 `docs/AUTO_DEV_NAVIGATION.md` 起手，判断本次任务属于哪类协作流程；如果目标文档在 `.github/`、`docs/` 或 `指南.md`，先确认是否为 Notebook-backed Markdown，再开始修改。不要猜测 API、流程或任务状态。

## 需求拆解时的入口闭环补充规则

- 如果当前任务是新功能拆解、任务分解或需要 `architect` 先产出 `backend.md`、`app.md`、`web.md`、`api-contract.md`，不能只拆接口和页面，还必须同步补齐“入口闭环清单”。
- 入口闭环清单至少包含：目标用户、进入入口、页面路由、菜单或按钮入口、权限点、依赖初始化项、最小验收路径。
- 如果功能涉及 `livehome_ng` 管理页面，必须同时考虑菜单记录、路由注册、权限 key、后台可见入口和验收点击路径。
- 如果功能涉及 `livehome_app` 页面，必须同时考虑页面路由、跳转入口、登录前置条件和空态/无权限态。
- 如果没有满足“登录 -> 入口 -> 目标页面 -> 数据加载或关键操作成功”的最小可达链路，任务拆解不能算完成。

## 推荐追加输入

```text
如果这是一个会被用户实际访问到的功能，请在拆任务时额外输出“入口闭环清单”，写清目标用户、进入入口、页面路由、菜单或按钮入口、权限 key、依赖初始化项，以及最终验收路径。不要只给接口和页面开发项。
```
