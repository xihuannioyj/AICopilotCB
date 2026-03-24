# 任务派发索引

## 文档定位

- machine_readable_tag: aicopilotcb-task-dispatch-index-v1
- 文档角色：判断任务属于当前开发窗口、候选池还是治理专项的唯一人工派发入口

## 使用顺序

1. 先判断任务是否属于业务开发还是治理维护。
2. 当前开发窗口内的业务任务进入 `tasks/task-list.md`。
3. 未进入当前窗口的候选任务进入 `tasks/task-backlog.md`。
4. Prompt、Agent、Hook、Runbook、守卫脚本等治理专项进入 `tasks/governance-task-list.md`。

## 当前开发窗口

- 当前窗口状态：未初始化具体业务任务
- 读取顺序：先看本索引，再看目标主看板，再看 feature 目录任务文档

## 候选池入口

- 统一写入 `tasks/task-backlog.md`

## 治理专项入口

- 统一写入 `tasks/governance-task-list.md`
