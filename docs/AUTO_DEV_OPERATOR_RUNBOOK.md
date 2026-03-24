# AUTO_DEV 操作员 Runbook

## 文档定位

- machine_readable_tag: aicopilotcb-auto-dev-operator-runbook-v1
- 文档角色：为值班、盘点、操作员收口提供固定执行顺序

## 启动前检查

1. 读取 `docs/AUTO_DEV_NAVIGATION.md`，确认当前场景属于 readiness、汇报还是演练。
2. 读取 `tasks/_runtime/task-index.json`，确认 runtime 主数据是否存在。
3. 读取 `tasks/task-list.md`、`tasks/task-backlog.md`、`tasks/governance-task-list.md`，确认人工主看板是否与当前场景匹配。
4. 若要输出结论，先读取 `docs/AUTO_DEV_COMPLETE_READINESS_CHECKLIST.md`。

## 值班执行顺序

1. 先看 runtime 主数据是否完整。
2. 再看是否存在当前窗口业务任务、候选池任务、治理专项任务混写。
3. 再看是否存在受保护 Markdown 写入失败、缺失校验或结构损坏迹象。
4. 最后决定输出的是 readiness 结论、进度摘要还是风险提示。

## 收尾要求

- 输出必须区分：已确认事实、仍待补证的判断、下一步动作。
- 若当前只具备人工主看板数据，不得伪装成 runtime 自动结论。
- 若当前只有 runtime 占位数据，不得伪装成系统已经 fully operational。
