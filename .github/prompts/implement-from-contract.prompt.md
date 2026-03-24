---
description: 前端/App AI工程师快捷指令：根据 api-contract.md 生成对应的 Service 调用代码和 Model 定义。 在 Flutter 或 Angular 对话中，打开任务文件后使用。
---

# 根据 API 契约生成对接代码

## 统一沟通语言

- 本 Prompt 产出的所有用户可见回复必须统一使用简体中文。
- 不要在正常叙述中混用英文、日文、韩文或繁体中文作为主语言。
- 代码标识符、命令、路径、字段名、报错原文，以及用户明确要求引用的原文内容，可以按原样保留。
- 需要保留非简体中文原文时，必须先给出简体中文解释，再附最小必要原文。

## 使用方式

告诉我要对接哪个功能，我会：

1. 读取 `tasks/{功能名}/api-contract.md`
2. 根据你的技术栈（Flutter 或 Angular）生成对接代码

## 不适用场景

- 如果当前任务属于 AI 协同方案维护任务，例如只修改 Prompt、Agent、Hook、Instructions、指南、任务模板或其他协作文档，则**不要**使用本 Prompt。
- `implement-from-contract` 只用于后端契约已经明确、且需要生成 Flutter 或 Angular 对接代码时。
- 方案维护任务应直接修改协作规则与文档，不应进入代码生成流程。

## 如果是 Flutter（livehome_app）

自动生成：

- __Model 类__（`lib/models/{name}_model.dart`）含 `fromJson` 工厂方法
- __Service 方法__（`lib/services/{name}_service.dart`）封装每个 API 的 Dio 调用
- **BLoC 骨架**（如果任务文件要求状态管理）

## 如果是 Angular（livehome_ng）

自动生成：

- **TypeScript 接口定义**（`src/app/models/{name}.model.ts`）
- **Service 方法**（`src/app/services/{name}.service.ts`）
- **Component 骨架**（含 NzTable 分页、搜索表单、操作按钮）

## 检查要点

生成前先确认：

- [ ] `api-contract.md` 状态标记为 ✅（后端已实现）
- [ ] 接口 URL 与项目约定前缀一致（`/api/v1/` 或 `/api/v1/admin/`）
- [ ] 字段命名使用蛇形命名法（`user_name` 而非 `userName`）
- [ ] 响应结构按 `{code, message, data}` 对齐
- [ ] Angular 输出遵守 Standalone + OnPush + `inject()`；Flutter 输出遵守 BLoC + Service 分层

## 字段级契约前置条件

- 只有当 `api-contract.md` 完整到无需猜字段时，才允许基于契约生成 Flutter 或 Angular 对接代码。
- 至少必须存在：

   1. 请求参数表
   2. 响应字段表
   3. JSON 响应示例
   4. `endpoint_scope`
   5. `lifecycle_status`

- 如果缺少以上任一项，必须先停止生成代码，并明确指出契约缺口，不得基于猜测生成 Model、Service 或 Component。

## 生成前新增检查项

- [ ] `api-contract.md` 状态标记为 ✅（后端已实现）
- [ ] 已包含请求参数表
- [ ] 已包含响应字段表
- [ ] 已包含 JSON 响应示例
- [ ] 字段名、类型、状态值、可空规则足够明确，无需前端猜测
