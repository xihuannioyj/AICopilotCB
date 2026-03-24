---
description: 后端AI工程师快捷指令：完成接口开发后，自动更新 api-contract.md 和任务文件状态。 在后端工程师对话中使用。
---

# 更新 API 契约文档

## 统一沟通语言

- 本 Prompt 产出的所有用户可见回复必须统一使用简体中文。
- 不要在正常叙述中混用英文、日文、韩文或繁体中文作为主语言。
- 代码标识符、命令、路径、字段名、报错原文，以及用户明确要求引用的原文内容，可以按原样保留。
- 需要保留非简体中文原文时，必须先给出简体中文解释，再附最小必要原文。

## 不适用场景

- 如果当前任务属于 AI 协同方案维护任务，例如只修改 Prompt、Agent、Hook、Instructions、指南、任务模板或其他协作文档，则**不要**使用本 Prompt。
- `update-api-contract` 只用于后端接口已经实现、需要把真实接口信息回写到 `api-contract.md` 时。
- 方案维护任务应直接修改协作规则、流程文档与模板，不应进入 API 契约回写流程。

你刚刚完成了一个 API 接口的开发。请执行以下步骤：

## Step 1：确认任务文件

在 `tasks/` 目录下找到对应功能文件夹，检查 `api-contract.md` 是否存在。
如果不存在，按 Step 2 的格式新建文件。

## Step 2：更新 api-contract.md

对每个接口，按此格式记录：

```markdown
## {接口名称}

- **URL**：`{实际路由路径}`
- **Method**：`GET | POST | PUT | DELETE`
- **Auth**：`Bearer Token`
- **权限**：`{permission.slug}`（管理端接口需要）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| xxx  | string | 是 | xxx |

{"code": 200, "message": "操作成功", "data": {}}

| code | message | 触发条件 |
|------|---------|---------|
| 400 | xxx | xxx |
```

## Step 3：标记任务状态

在 `backend.md` 的任务清单中，将对应条目标记为 `[x]`。

## Step 4：更新契约状态

在 `api-contract.md` 顶部更新状态标记：

```ini
> 状态：✅ 后端已实现，前端可对接
> 更新时间：{今天日期}
```

## Step 5：进入收尾闭环

- 如果当前功能的 `backend.md` 已全部完成，继续执行 `.github/prompts/close-feature.prompt.md`
- 收尾前再次确认响应示例统一使用 `{code, message, data}`，不要混用 `msg`

## Step 2.5：字段级契约完整性检查

- `api-contract.md` 只有接口路径、Method、治理标签，**不算完成**。
- 更新契约时，对每个可对接接口必须至少补齐以下内容：

   1. `endpoint_scope`
   2. `lifecycle_status`
   3. `permission_key`（管理端受保护接口）
   4. `controller_action`
   5. 请求参数表
   6. 响应字段表
   7. JSON 响应示例
   8. 错误码或失败场景说明

- 如果是历史接口治理任务，还必须补齐：

   1. `old_to_new_mapping`
   2. `migration_condition`
   3. `deprecation_condition`

## 字段级契约输出格式

### 请求参数表

| 参数名 | 类型 | 必填 | 位置 | 说明 |
|--------|------|------|------|------|
| `id` | `int` | 是 | path | 主键 ID |

### 响应字段表

| 字段路径 | 类型 | 可空 | 说明 |
|----------|------|------|------|
| `code` | `int` | 否 | 业务状态码 |
| `message` | `string` | 否 | 响应消息 |
| `data.id` | `int` | 否 | 主键 ID |

### JSON 响应示例

```json
{
  "code": 200,
  "message": "操作成功",
  "data": {
    "id": 1
  }
}

```

## 可对接状态判定

- 只有当 `api-contract.md` 至少包含“请求参数表 + 响应字段表 + JSON 响应示例”时，才允许把状态更新为“前端可对接”。
- 如果缺少其中任一项，只能标记为“后端代码已完成，契约待补全”，不得通知 Flutter 和 Angular 开工。
