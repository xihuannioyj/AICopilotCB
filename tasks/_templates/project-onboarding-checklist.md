# 新项目接入检查模板

## 文档定位

- machine_readable_tag: aicopilotcb-project-onboarding-checklist-template-v1
- 文档角色：为新项目装配提供最小检查清单和落盘模板

## 基本信息

- 项目名称：{project-name}
- 项目类型：{control-plane / backend / app / web / mixed}
- 技术栈：{stacks}
- 目标根目录：{root-path}

## 接入步骤

1. 已选择对应 `stacks/` 作为接入起点。
2. 已在 `projects/{project-name}/` 建立覆盖层目录。
3. 已确认 `workspace-init.json` 中的项目默认配置。
4. 已确认 `role-boundaries.json` 中的角色默认边界。
5. 已确认 `active-context.json` 是否需要新增 profile 或实例覆盖。
6. 已确认 `tasks/` 主看板、候选池、治理表与 runtime 路径是否对齐。
7. 已执行至少一次 guard 校验与最小演练。

## 验证结果

- Prompt 分流：{ok / pending}
- Agent 边界：{ok / pending}
- Markdown 写入：{ok / pending}
- 任务板路径：{ok / pending}
- runtime 占位：{ok / pending}

## 风险与待办

- {risk-or-todo}
