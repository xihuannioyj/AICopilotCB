# 受控执行演练 Runbook

## 文档定位

- machine_readable_tag: aicopilotcb-assisted-drill-runbook-v1
- 文档角色：规范受控半自动执行演练的前置条件、执行顺序与收尾要求

## 前置条件

1. 已确认当前场景属于受控演练，而不是直接生产执行。
2. 已明确数据来源和演练目标。
3. 已准备记录模板和结论模板。

## 执行顺序

1. 读取 `docs/AUTO_DEV_NAVIGATION.md`。
2. 读取 `docs/AUTO_DEV_COMPLETE_READINESS_CHECKLIST.md`，确认当前是否具备演练基础。
3. 使用 `docs/ASSISTED_EXECUTION_DRILL_RECORD_TEMPLATE.md` 记录步骤与观察结果。
4. 使用 `docs/ASSISTED_EXECUTION_DRILL_CONCLUSION_TEMPLATE.md` 输出结论。

## 收尾要求

- 结论必须区分：演练成功项、失败项、不可下结论项。
- 不得把演练结果直接表述为生产可用结论。
