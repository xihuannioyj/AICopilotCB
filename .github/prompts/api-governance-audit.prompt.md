---
description: 对 livehome_admin 接口执行治理审计，识别双轨边界、历史接口问题与整改优先级。
mode: ask
---

# 管理端 API 治理审计与整改

## 统一沟通语言

- 本 Prompt 产出的所有用户可见回复必须统一使用简体中文。
- 不要在正常叙述中混用英文、日文、韩文或繁体中文作为主语言。
- 代码标识符、命令、路径、字段名、报错原文，以及用户明确要求引用的原文内容，可以按原样保留。
- 需要保留非简体中文原文时，必须先给出简体中文解释，再附最小必要原文。

## 不适用场景

- 如果当前任务属于 AI 协同方案维护任务，例如只修改 Prompt、Agent、Hook、Instructions、指南、任务模板或其他协作文档，则**不要**使用本 Prompt。
- `api-governance-audit` 只用于 `livehome_admin` 管理端历史接口、双轨接口、REST 化与权限治理的审计。
- 方案维护任务应直接修改协作方案文件，不应伪装成接口治理审计。

## 输出格式

### 3. 不合规项

每条问题必须包含：

- `method`
- `path`
- `controller_action`
- `endpoint_scope`
- `问题类型`
- `原因`

## 使用场景

- 当任务目标是审计 `livehome_admin` 管理端历史接口、双轨接口边界、REST 化缺口、权限点缺失或命名治理问题时，使用本 Prompt。
- 本 Prompt 的输出是审计结论和整改清单，不是直接改代码。

## 必读范围

开始前至少应读取：

1. `livehome_admin/routes/api_admin.php`
2. 涉及模块的 Controller
3. 如有对应契约，再读取 `tasks/{feature-name}/api-contract.md`
4. `.github/copilot-instructions.md` 中的管理端 API 治理规则与双轨接口制度

## 审计维度

至少从以下维度逐项检查：

1. 路径命名是否仍在新增下划线动作式接口。
2. 接口是否属于 `web-admin`、`flutter-app` 或 `shared`，有没有混用。
3. 历史接口是否已标记 `primary`、`compatibility`、`deprecated`。
4. 受保护接口是否显式绑定权限点。
5. permission key 是否符合 `admin.{module}.{resource}.{action}`。
6. 是否存在应改为 REST 风格却仍停留在 `save/details/remove/set` 风格的新增接口。
7. 契约是否缺少 `endpoint_scope`、`lifecycle_status`、`permission_key`、`controller_action`、`old_to_new_mapping`、`migration_condition`、`deprecation_condition`。

## 输出格式补充

### 1. 审计范围

- 审计模块
- 涉及路由文件
- 涉及 controller_action

### 2. 合规项

- 已符合治理规则的路径、权限或契约点

### 3. 不合规项

每条问题至少写清：

- `method`
- `path`
- `controller_action`
- `endpoint_scope`
- `问题类型`
- `原因`
- `建议整改方向`

### 4. 整改优先级

- P0：必须先处理的问题
- P1：应在本轮治理中处理的问题
- P2：可排入后续治理批次的问题

### 5. 是否进入治理规划

最后给出明确结论：

- 可直接进入 `.github/prompts/api-governance-refactor-plan.prompt.md`
- 还不能进入治理规划，需先补审计证据

## 关键约束

- 审计必须基于真实路由和 controller，不得凭空列问题。
- 审计阶段不要直接进入代码修改。
- 审计阶段若发现只是协同方案维护任务，应停止使用本 Prompt。
