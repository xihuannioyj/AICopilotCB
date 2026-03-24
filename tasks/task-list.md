# 当前开发项目任务总表

## 文档定位

- machine_readable_tag: aicopilotcb-task-list-v1
- 文档角色：当前开发窗口内业务任务的唯一人工主看板

## 使用规则

- 只登记已经进入当前开发窗口的业务任务。
- 治理专项不进入本表，统一写入 `tasks/governance-task-list.md`。
- 待排期或长期候选任务不进入本表，统一写入 `tasks/task-backlog.md`。
- 运行态自动编排结果以 `tasks/_runtime/task-index.json` 为准，本表只承担人工主状态。

## 当前窗口状态

- 当前状态：未初始化具体业务任务
- 维护角色：architect 创建任务块，相关 Agent 在开始与收尾时回写自己的状态

## Agent 总览

| Agent | 当前负责任务块 | 当前状态 | 最新说明 |
|-------|----------------|----------|----------|
| product-manager | 未启用 | 未启用 | 当前无业务需求澄清任务 |
| architect | 未开始 | 未开始 | 等待拆解具体业务任务 |
| backend | 未开始 | 未开始 | 等待进入具体业务窗口 |
| flutter | 未开始 | 未开始 | 等待进入具体业务窗口 |
| angular | 未开始 | 未开始 | 等待进入具体业务窗口 |
| test-collector | 未启用 | 未启用 | 等待出现联调采证场景 |
| defect-triage | 未启用 | 未启用 | 等待出现 findings 输入 |
| doc-manager | 未启用 | 未启用 | 等待进入文档收口阶段 |

## 任务卡片模板

### {feature-name}

| 字段 | 内容 |
|------|------|
| 所属功能目录 | `{feature-name}` |
| 任务名称 | {task-name} |
| 中文描述 | {summary} |
| 当前状态 | {未开始 / 开发中 / 待联调 / 待测试 / 待评审 / 已完成 / 已阻塞 / 未启用} |
| 预估完成周期 | {eta} |
| 下一动作 | {next-step} |

| Agent角色 | 完成状态 | 遇到问题 |
|-----------|----------|----------|
| product-manager | 未启用 | {issue} |
| architect | 未开始 | {issue} |
| backend | 未开始 | {issue} |
| flutter | 未开始 | {issue} |
| angular | 未开始 | {issue} |
| test-collector | 未启用 | {issue} |
| defect-triage | 未启用 | {issue} |
| doc-manager | 未启用 | {issue} |

