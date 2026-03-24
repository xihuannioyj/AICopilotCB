# AUTO_DEV 导航

## 文档定位

- machine_readable_tag: aicopilotcb-auto-dev-navigation-v1
- 文档角色：方案运营、值班、盘点、汇报与演练场景的统一导航入口
- 适用范围：readiness 检查、日报周报、管理摘要、风险收口、受控演练、操作员值班

## 入口分流

1. 要判断当前控制面是否可继续推进、试运行或完全可用：读取 `docs/AUTO_DEV_COMPLETE_READINESS_CHECKLIST.md`。
2. 要执行值班、日常巡检或收口操作：读取 `docs/AUTO_DEV_OPERATOR_RUNBOOK.md`。
3. 要产出日报、周报、里程碑、风险台账或管理摘要：使用 `docs/AUTO_DEV_*_TEMPLATE.md`。
4. 要做受控半自动演练：读取 `docs/ASSISTED_EXECUTION_DRILL_RUNBOOK.md`，并配套使用记录模板和结论模板。

## 数据来源优先级

1. runtime 主数据：`tasks/_runtime/task-index.json`
2. runtime 报表：`tasks/_runtime/reports/*.json`
3. 人工主看板：`tasks/task-list.md`、`tasks/task-backlog.md`、`tasks/governance-task-list.md`
4. 需求与规则来源：`docs/requirements/`、`.github/copilot-instructions.md`

## 模板清单

- `docs/AUTO_DEV_DAILY_REPORT_TEMPLATE.md`
- `docs/AUTO_DEV_WEEKLY_REPORT_TEMPLATE.md`
- `docs/AUTO_DEV_MILESTONE_TEMPLATE.md`
- `docs/AUTO_DEV_RISK_REGISTER_TEMPLATE.md`
- `docs/AUTO_DEV_MANAGEMENT_SUMMARY_TEMPLATE.md`

## 演练与检查清单

- `docs/AUTO_DEV_OPERATOR_RUNBOOK.md`
- `docs/AUTO_DEV_COMPLETE_READINESS_CHECKLIST.md`
- `docs/ASSISTED_EXECUTION_DRILL_RUNBOOK.md`
- `docs/ASSISTED_EXECUTION_DRILL_RECORD_TEMPLATE.md`
- `docs/ASSISTED_EXECUTION_DRILL_CONCLUSION_TEMPLATE.md`

## 使用要求

- 任何 readiness、日报、周报、里程碑或管理摘要，都必须显式写明数据来自 runtime、人工主看板还是候选池。
- 若多个来源同时使用，必须分别说明每个来源负责解释什么，禁止把不同来源混成单一结论。
- 该导航只负责分流，不替代具体模板或 Runbook 承载完整细则。
