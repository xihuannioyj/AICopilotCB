# AI 协同方案维护

## 使用场景

- 当任务目标是完善或修复 AI 协同方案本身时，使用本 Prompt。
- 典型场景包括：修改 Prompt、Agent、Hook、Instructions、指南、任务模板、协作文档、校验规则、方案闭环流程。
- 如果任务目标是业务功能开发、接口实现、页面实现、BLoC/Service/Controller 编码，则不要使用本 Prompt，应切换到对应业务 Prompt 或业务 Agent。

## 默认边界

- 默认只允许修改 `.github/`、`docs/`、`指南.md`、任务模板、协作文档与方案校验脚本。
- 未经用户明确要求，不要顺手修改 `livehome_admin/`、`livehome_app/`、`livehome_ng/` 中的业务代码、页面、接口实现、测试或迁移。
- 如果发现业务代码现状会影响方案设计，只做只读核查，并把结果沉淀为规则、风险、约束、证据或后续建议。

## 与其他入口的关系

- 如果用户只是希望“每次新开 Chat 都先严格吃到仓库规则”，先用 `.github/prompts/workspace-chat-start.prompt.md` 起手；完成分流后再切回本 Prompt。
- 如果当前目标是判断 readiness、值班交接、阶段验收或管理层汇报前状态，优先使用 `.github/prompts/auto-dev-readiness-check.prompt.md`，不要在本 Prompt 里直接给出 readiness 结论。
- 如果当前目标是启动业务需求、组织 8 Agent 分工、拆任务文档并推进三端交付，优先使用 `.github/prompts/eight-agent-collaboration-kickoff.prompt.md`。
- `tasks/_runtime/` 下的模板、schema、报表消费协议，以及 `scripts/auto_dev_*`、`scripts/ai_workspace_guard.py` 这类控制面脚本，只要用户目标是“完善 AI 协作方案本身”，都属于本 Prompt 的治理范围。

本 Prompt 解决的是“规则、入口、模板、控制面和协作文档本身”的问题；它不替代业务开发 Prompt，也不替代 readiness 检查入口。

## 统一沟通语言

- 方案维护任务中的所有用户可见回复，必须统一使用简体中文。
- 不要把英文、日文、韩文或繁体中文混入正常叙述正文。
- 代码标识符、命令、路径、字段名、报错原文与用户明确要求引用的原文内容，可以保留原样。
- 需要附原文时，先给简体中文解释，再附最小必要原文。

## 执行目标

你要做的是让协同方案变得：

1. 更清晰：职责边界、入口路由、适用场景、不适用场景明确。
2. 更可执行：Prompt、Agent、Instructions、Hook、文档之间不打架。
3. 更可校验：方案改动后能通过文件安全校验，并尽量能通过规则检查发现回归。
4. 更少误用：避免方案维护任务误进入业务实现流程，避免业务实现任务误走方案维护路径。

## 必做步骤

1. 先判断当前需求属于哪类方案维护：

   - Prompt 路由补齐
   - Agent 边界补齐
   - Instructions 规则修订
   - Hook/校验规则增强
   - 指南/模板/任务文档补齐
   - 全局一致性检查

2. 读取相关方案文件，优先关注：

   - `.github/copilot-instructions.md`
   - `.github/instructions/`
   - `.github/agents/`
   - `.github/prompts/`
   - `.github/hooks/`
   - `指南.md`
   - `tasks/` 下的模板类文件（如适用）

3. 明确本次修改边界，只在必要文件中做最小变更。
4. 修改后执行文件安全校验：

   - `python scripts/ai_workspace_guard.py validate-changed --root . --json`

5. 如果本次改动涉及方案级流程或全局约束，额外执行：

   - `python scripts/ai_workspace_guard.py validate-project --root . --scope backend --scope app --scope web --json`

6. 如相关 Hook 会覆盖本次规则，再补做 Hook 级复核，确保方案不会互相冲突。

## 输出要求

输出结果至少应包含：

1. 本次维护目标
2. 修改文件清单
3. 规则变更说明
4. 校验结果
5. 剩余缺口与下一步建议

## 标准输入示例

### 示例 1：补齐 Prompt 分流边界

用户输入示例：

- 请继续完善 AI 协同方案。
- 目标：给剩余 Prompt 补齐“方案维护任务不适用”说明。
- 约束：只允许修改 `.github/prompts/` 和相关说明文档，不要改业务代码。

### 示例 2：做一轮方案一致性检查

用户输入示例：

- 请检查当前协同方案是否还存在规则冲突或漏配。
- 重点检查：`copilot-instructions`、`instructions`、`agents`、`prompts`、`hooks` 是否一致。
- 如果有缺口，直接补齐并做校验。

## 标准输出示例

输出应尽量采用这种结构：

1. 本次维护目标
2. 修改文件清单
3. 每个文件新增或修正的规则
4. 已执行的校验命令与结果
5. 仍待处理的边界、风险或下一步建议

### 输出示例

- 本次目标：补齐方案维护任务的 Prompt 分流边界。
- 修改文件：`.github/prompts/feature-done-check.prompt.md`、`.github/prompts/update-api-contract.prompt.md`。
- 规则变更：新增“不适用场景”，明确方案维护任务不能误入业务 Prompt。
- 校验结果：已执行 `python scripts/ai_workspace_guard.py validate-changed --root . --json`，结果为 `status=ok`。
- 后续建议：继续补齐 Agent 边界或新增专用方案维护入口。

## 标准任务清单模板

当需要把方案维护任务拆成可执行清单时，输出可尽量采用以下结构：

### 任务清单模板

1. 维护目标

   - 本轮要补的方案能力是什么

2. 影响范围

   - 会改哪些 Prompt / Agent / Instructions / Hook / 指南 / 模板

3. 边界约束

   - 哪些业务目录明确不改

4. 执行动作

   - 先改什么
   - 再改什么
   - 最后做什么校验

5. 验收标准

   - 哪些规则补齐后才算完成

6. 校验命令

   - `python scripts/ai_workspace_guard.py validate-changed --root . --json`
   - 如涉及全局流程，再执行 `python scripts/ai_workspace_guard.py validate-project --root . --scope backend --scope app --scope web --json`

### 任务清单示例

1. 维护目标

   - 补齐方案维护任务的入口、分流与反例说明

2. 影响范围

   - `.github/prompts/maintain-collaboration-scheme.prompt.md`
   - `.github/copilot-instructions.md`
   - `指南.md`

3. 边界约束

   - 不修改 `livehome_admin/`、`livehome_app/`、`livehome_ng/` 业务代码

4. 执行动作

   - 先补 Prompt 示例与反例
   - 再补全局入口说明
   - 最后回写指南中的人工使用方法

5. 验收标准

   - 用户能明确知道何时进入方案维护模式
   - AI 能明确知道何时不该进入业务 Prompt

6. 校验命令

   - `python scripts/ai_workspace_guard.py validate-changed --root . --json`

## 输出分级标准

当方案维护任务规模不同时，输出粒度应随之调整：

### 级别 A：轻量修订

适用场景：

- 只补 1 到 2 处规则说明
- 只修单个 Prompt / Agent / Instructions 的边界或措辞
- 不涉及全局路由变化

输出要求：

1. 直接说明修改项
2. 列出修改文件
3. 给出 `validate-changed` 结果

### 级别 B：结构修订

适用场景：

- 同时修改多个 Prompt / Agent / Instructions
- 涉及入口、分流、边界、模板结构调整
- 需要补一套示例、反例、任务模板或统一约束

输出要求：

1. 说明维护目标
2. 分文件说明规则变更
3. 说明边界约束
4. 给出 `validate-changed` 结果
5. 如相关，补充 Hook 复核结果

### 级别 C：全局审计

适用场景：

- 需要检查 Prompt、Agent、Instructions、Hook、指南之间是否冲突
- 需要判断方案是否已达到稳定使用状态
- 需要输出剩余缺口、风险和后续治理顺序

输出要求：

1. 先给综合结论
2. 再列出问题或缺口
3. 按优先级排序
4. 列出建议修复顺序
5. 给出 `validate-changed`、`validate-project` 与 Hook 结果

### 默认选择规则

- 如果只是局部补充，按级别 A 输出。
- 如果涉及多个方案文件联动，按级别 B 输出。
- 如果用户明确要求“整体看看还差多少”“做一致性检查”“评估是否完全可用”，按级别 C 输出。

## 最终交付口径

当一次方案维护任务结束时，最终结论建议统一采用以下结构：

### 标准结论结构

1. 本轮维护结论

   - 例如：本轮属于级别 A / B / C，目标已完成 / 部分完成

2. 已完成项

   - 明确列出本轮已落地的规则、入口、边界、示例、模板或校验项

3. 校验结论

   - 明确列出 `validate-changed` 结果
   - 如有执行，再列出 `validate-project` 与 Hook 结果

4. 剩余缺口

   - 如果还有未覆盖内容，必须明确写出

5. 下一步建议

   - 只给与当前方案演进直接相关的建议

### 推荐表达示例

- 本轮维护结论：本轮属于级别 B 结构修订，方案维护入口、分流规则与使用说明已补齐。
- 已完成项：已补 Prompt 入口、标准反例、任务模板、输出分级标准，并在指南中补齐使用说明与决策表。
- 校验结论：`validate-changed` 已通过；Hook 复核结果为 `continue=true`。
- 剩余缺口：暂无阻断项；若继续提升，可补更细的治理清单或目录整理。
- 下一步建议：只在确有需要时再补更细粒度的交付模板或审计清单。

### 禁止口径

- 不要使用“应该差不多可以了”“大概没问题”这类模糊结论。
- 不要在未校验时输出“已完全可用”。
- 不要把方案维护结论和业务功能完成结论混写在一起。

## 标准反例

以下请求**不应**使用本 Prompt，而应切换到业务 Prompt、业务 Agent 或专项治理 Prompt：

### 反例 1：直接做后端接口开发

用户输入示例：

- 请帮我在 `livehome_admin` 新增一个标签批量删除接口。

原因：这是后端业务实现任务，应走后端开发流程，而不是方案维护流程。

### 反例 2：直接做 Flutter 页面开发

用户输入示例：

- 请根据 `tasks/user-checkin/app.md` 开始实现签到页面。

原因：这是 Flutter 业务实现任务，应读取任务文件和 `api-contract.md` 后进入 App 开发流程。

### 反例 3：直接做 Angular 管理后台页面开发

用户输入示例：

- 请把敏感词管理页面补成可搜索、可分页、可新增编辑。

原因：这是 Angular 业务实现任务，应走 Web 开发流程，而不是修改协同方案。

### 反例 4：直接做 API 治理专项

用户输入示例：

- 请审计 `livehome_admin` 里所有历史动作式接口，并给出双轨整改计划。

原因：这是治理专项任务，应优先使用 `api-governance-audit.prompt.md` 或 `api-governance-refactor-plan.prompt.md`。

## 判定标准

- 如果本次需求明确是方案维护任务，却仍把主要精力放在业务代码实现上，视为执行偏航。
- 如果新增规则与现有 Prompt、Agent、Instructions、Hook 存在冲突，视为方案未完成。
- 如果改动后未执行 `validate-changed`，视为收尾不完整。
- 若涉及全局流程变更却未检查项目级影响，视为验证不足。
