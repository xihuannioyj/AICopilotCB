---
description: 功能完成质检。检查一个功能或治理任务是否满足上线前的完成定义。
mode: ask
---

# 功能完成定义（Definition of Done）质检

## 统一沟通语言

- 本 Prompt 产出的所有用户可见回复必须统一使用简体中文。
- 不要在正常叙述中混用英文、日文、韩文或繁体中文作为主语言。
- 代码标识符、命令、路径、字段名、报错原文，以及用户明确要求引用的原文内容，可以按原样保留。
- 需要保留非简体中文原文时，必须先给出简体中文解释，再附最小必要原文。

## 不适用场景

- 如果当前任务属于 AI 协同方案维护任务，例如只修改 Prompt、Agent、Hook、Instructions、指南、任务模板或其他协作文档，则**不要**使用本 Prompt。
- `feature-done-check` 只用于业务功能或治理任务进入完成定义验收阶段时的质检。
- 方案维护任务应直接检查 `.github/`、`docs/`、`指南.md` 等方案文件的一致性与可执行性，不应伪装成业务功能上线验收。

## 接口治理专项检查

- [ ] 新增 Web Admin 接口符合双轨制度
- [ ] 新增 Flutter 接口未继续使用 `save/details/remove/set`
- [ ] 涉及历史接口时，已标记 `primary`、`compatibility` 或 `deprecated`
- [ ] 已补齐 `endpoint_scope`、`lifecycle_status`、`permission_key`
- [ ] 已写明旧新接口映射、迁移条件、下线条件

## 输出格式

1. 通过项
2. 未通过项
3. 待确认项
4. 综合结论：`READY TO SHIP` 或 `需修复 N 项后才能上线`

## 字段级契约完整性检查

- 最终验收时，不能只检查 `api-contract.md` 是否存在，还必须检查它是否完整到“前端无需猜字段”的程度。
- 若某个功能需要 Flutter 或 Angular 对接，则对应接口至少应具备：

   1. 请求参数表
   2. 响应字段表
   3. JSON 响应示例
   4. `endpoint_scope`
   5. `lifecycle_status`

- 若为管理端受保护接口，还应具备：

   1. `permission_key`
   2. `controller_action`

- 若为治理任务，还应具备：

   1. `old_to_new_mapping`
   2. `migration_condition`
   3. `deprecation_condition`

## 文件安全与项目级质检

- 质检时必须显式检查文件安全，不得只看功能表现。
- 至少执行：`python scripts/ai_workspace_guard.py validate-changed --root . --json`。
- 如需判断仓库是否达到可发布基础状态，还必须执行：`python scripts/ai_workspace_guard.py validate-project --root . --scope backend --scope app --scope web --json`。
- 若 `validate-changed` 存在 `non_utf8`、`replacement_char`、`null_byte`、`invalid_json`，必须判定为未通过。
- 若 `validate-project` 存在失败检查，必须在“未通过项”中列出失败检查名称、范围与关键信息。
- 仅 `utf8_bom`、`missing_final_newline` 这类警告若仍存在，也必须进入“待确认项”或“未通过项”，不能静默忽略。

## 字段级契约未通过判定

- 出现以下任一情况，必须判定为未通过：
   - `api-contract.md` 只有接口路径或治理标签，没有字段级契约
   - 没有请求参数表
   - 没有响应字段表
   - 没有 JSON 响应示例
   - 字段名称、状态值、可空规则仍需要前端自行猜测
   - Backend 已改真实返回结构，但契约未同步更新
   - `validate-changed` 仍存在阻断级文件安全问题
   - `validate-project` 仍存在阻断性失败检查

## 输出要求补充

- 在“未通过项”中，必须单独列出字段级契约缺失的接口或文件。
- 在“未通过项”中，必须单独列出文件安全问题与项目级失败检查。
- 如果字段级契约不完整，综合结论不得输出 `READY TO SHIP`。
- 如果文件安全或项目级检查未通过，综合结论不得输出 `READY TO SHIP`。
- 只有当实现代码、任务文档、字段级契约、文件安全、项目级检查五者一致时，才允许输出 `READY TO SHIP`。

## 页面可达性与入口闭环检查

如果功能面向后台用户、App 用户或任何最终用户可见页面，Definition of Done 质检必须额外检查：

- [ ] 页面路由已注册
- [ ] 存在真实入口，例如菜单、按钮、卡片或跳转链路
- [ ] 权限 key、菜单可见性、接口权限控制一致
- [ ] 依赖的菜单数据、初始化数据、字典、配置项已落地
- [ ] 可以按“登录 -> 点击入口 -> 进入页面 -> 数据加载或关键操作成功”走通最小验收路径

## 入口闭环未通过判定

- 出现以下任一情况，必须判定为未通过：
   - 页面文件已存在，但路由未注册
   - 页面路由已存在，但没有菜单、按钮或其他真实入口
   - 菜单或入口已存在，但权限 key、权限控制或菜单可见条件不一致
   - 依赖数据库菜单、字典、初始化数据，但仓库中没有实际落地证据
   - 页面只能由开发者手工输入地址访问，正常用户无法按产品路径进入
   - 接口与页面都完成，但最小验收路径无法走通

## 输出要求补充

- 在“未通过项”中，必须单独列出入口闭环缺失点，例如缺路由、缺菜单、缺权限、缺初始化数据、缺验收路径。
- 只有当代码实现、字段级契约、入口闭环、文件安全、项目级检查五者一致时，才允许输出 `READY TO SHIP`。
