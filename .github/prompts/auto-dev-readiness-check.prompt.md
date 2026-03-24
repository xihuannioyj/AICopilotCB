# 自动编排 Readiness 检查

## 统一沟通语言

- 本 Prompt 产出的所有用户可见回复必须统一使用简体中文。
- 不要在正常叙述中混用英文、日文、韩文或繁体中文作为主语言。
- 代码标识符、命令、路径、字段名、报错原文，以及用户明确要求引用的原文内容，可以按原样保留。
- 需要保留非简体中文原文时，必须先给出简体中文解释，再附最小必要原文。

## 使用场景

- 当你要判断当前 AI 协作方案是否已经达到“可继续推进、可进入试运行、或可判定为完全可用”时，优先使用本 Prompt。
- 当你要做值班交接、运行盘点、阶段验收、管理层汇报前的状态确认时，也优先使用本 Prompt。
- 本 Prompt 不用于业务功能开发，不用于补接口，不用于页面编码。

## 不适用场景

- 如果当前任务是业务代码开发、接口实现、Flutter 或 Angular 页面联调，不要使用本 Prompt。
- 如果当前任务是完善 Prompt、Agent、Hook、Instructions、指南、模板等协同方案本身，优先使用 `.github/prompts/maintain-collaboration-scheme.prompt.md`。
- 如果当前任务是执行半自动演练或受控操作，先看 `docs/ASSISTED_EXECUTION_DRILL_RUNBOOK.md`，不要把 readiness 检查当成执行动作本身。

## 必读来源

开始判断前，必须先读取以下真实来源，不允许脱离运行态报表口头判断：

1. `tasks/_runtime/reports/latest-system-readiness.json`
2. `tasks/_runtime/reports/latest-watch-state.json`
3. `tasks/_runtime/reports/latest-batch-validation-summary.json`
4. `tasks/_runtime/task-index.json`
5. `docs/AUTO_DEV_OPERATOR_RUNBOOK.md`
6. `docs/AUTO_DEV_COMPLETE_READINESS_CHECKLIST.md`

如需确认控制面规则，可补读：

- `.github/auto-dev.json`
- `scripts/auto_dev_orchestrator.py`
- `scripts/auto_dev_review_queue.py`
- `scripts/auto_dev_manual_approval.py`

## 你的任务

你要把当前自动编排状态整理成可复核结论，至少回答四个问题：

1. 当前 readiness 所处阶段是什么。
2. 当前最大的阻塞项是什么。
3. 当前是否已经满足“完全可用”判定。
4. 下一步最该做的动作是什么。

## 检查顺序

1. 先看 `latest-system-readiness.json` 的 `summary.readinessScore`、`summary.readinessStage`、`summary.validationHealth`、`summary.taskDocClosure`、`summary.manualApproval`、`summary.assistedExecution`、`summary.reviewQueue`、`summary.watchLoop`。
2. 再看 `summary.validationHealth.failureCategories`、`summary.validationHealth.recommendedRecoveryActions`、`operatorActionQueue` 与 `gapToReady.failingValidationCategories`，先把环境缺失、脚本损坏和普通失败分开。
3. 如果这轮是 `--watch` 或怀疑 orchestrator 只是在空转，再看 `summary.watchLoop.consecutiveIdleRounds`、`summary.watchLoop.stopReason`、`summary.watchLoop.remainingTasks`，并用 `latest-watch-state.json` 对照 `lastActivityRound`、`lastActivityType` 与 `nextAction`。
4. 再看 `gapToReady.checklist` 是否满足：`allTasksDone`、`validationsGreen`、`taskDocsClosed`、`approvalsResolved`、`noBlockedTasks`。
5. 再看 `blockers`、`nextMilestones`，识别当前最直接的推进障碍。
6. 再从 `latest-batch-validation-summary.json` 核对 `overall`、`failures`、`failureCategories`、`recommendedRecoveryActions`、`groupedSummary.byFeatureValidation`。
7. 最后从 `task-index.json` 核对 `blocked`、`review_required`、`ready`、`done` 的实际分布，避免只看汇总分数下结论。
8. 对 `review_required` 必须继续分桶判断：先看 `validationScriptBlocked`、再看 `validationEnvironmentBlocked`、再看 `validationBlocked`、再看 `approvalPending`、最后才看 `assistedReady`。
9. 如果 `assistedExecution.readyToExecute` 大于 0，仍需结合 `summary.reviewQueue.assistedReady` 和 `python scripts/auto_dev_assisted_execution.py list` 二次确认，不得只凭一个汇总字段下结论。

## 判定规则

- 只要 `gapToReady.checklist` 中任一项不满足，就不能判定为“完全可用”。
- 只要 `validationHealth.overall` 不是 `passed`，就必须优先把失败校验列为主 blocker。
- 只要 `taskDocClosure.overall` 不是 `passed` 或 `taskDocsClosed` 不为 `true`，就说明任务文档仍不具备稳定支撑开发的闭环质量。
- 如果 `failureCategories` 中出现 `validation-script-defect`，要优先判断控制面依赖的测试资产是否已经损坏。
- 如果 `failureCategories` 中出现 `validation-environment-unavailable`，要优先判断本地服务、依赖进程或测试环境是否缺失。
- 如果 `operatorActionQueue` 已经给出动作清单，优先按它判断“当前最该做什么”，不要重新手工拼接 blockers。
- 如果 `recommendedRecoveryActions` 已给出步骤，优先按这些动作模板判断下一步，而不是重新猜测。
- 如果 `reviewQueue.validationScriptBlocked.count` 大于 0，说明 review_required 队列里存在被损坏脚本卡住的任务。
- 如果 `reviewQueue.validationEnvironmentBlocked.count` 大于 0，说明 review_required 队列里存在被环境缺失卡住的任务。
- 如果 `reviewQueue.validationBlocked.count` 大于 0，说明系统仍有未细分的普通失败校验阻塞。
- 如果任务仍落在任一 `validation*` 桶里，即使它同时满足 eligible 和 approved，也不能判定为可进入 assisted-execution。
- 如果 `assistedExecution.readyToExecute` 大于 0，说明已经存在可进入受控半自动执行窗口的任务，但这不等于整套方案已经完全可用。
- 如果 `manualApproval.pending` 大于 0，说明还有人工决策节点未闭环。
- 如果 `summary.watchLoop.watch = true` 且 `summary.watchLoop.consecutiveIdleRounds > 0`，同时 `summary.watchLoop.remainingTasks > 0`，要把它理解成“系统正在空转”，而不是“系统正在稳定推进”。
- 如果 `summary.watchLoop.stopReason = round-limit-reached` 但剩余任务仍多，优先回到 `operatorActionQueue` 和 `latest-review-queue.json` 看阻塞，不要只靠增加轮次掩盖问题。

## 输出要求

输出至少包含以下 5 段：

### 1. 当前结论

- readinessScore
- readinessStage
- 是否完全可用：是 / 否
- 一句话原因

### 2. 关键证据

- 从 readiness 报表摘出最关键字段
- 从 batch validation 报表摘出最关键字段
- 从 task-index 摘出最关键状态分布
- 明确写出 review_required 当前分流结论
- 明确写出 assisted-execution 当前是可进入、不可进入，还是暂无候选

### 3. blocker 清单

- blocker 名称
- 证据来源
- 影响范围
- 建议动作
- 如果 blocker 直接阻断 assisted-execution，要写明阻断原因

### 4. 下一步动作

按优先级列出 1 到 3 项，且必须是当前真实可执行动作。

### 5. 是否可进入下一阶段

结论只能在以下三种中选择一种：

- 继续加固，暂不建议扩大试运行
- 可控推进，可以继续受控试运行
- 已满足当前口径下的完全可用

## 输出约束

- 不得凭感觉给出 readiness 结论。
- 不得把“有 readyToExecute 任务”误判为“系统完全可用”。
- 不得跳过 `latest-batch-validation-summary.json` 只看 readiness 分数。
- 不得忽略 `review_required` 的分类差异。

## 推荐输入示例

请基于 `latest-system-readiness.json`、`latest-batch-validation-summary.json`、`task-index.json`、`docs/AUTO_DEV_OPERATOR_RUNBOOK.md` 和 `docs/AUTO_DEV_COMPLETE_READINESS_CHECKLIST.md`，给出当前自动编排方案的 readiness 结论、主 blocker、下一步动作，以及是否已经达到完全可用。
