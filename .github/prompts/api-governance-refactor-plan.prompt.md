---
description: 为双轨 API 治理生成母任务和模块拆分计划。
mode: ask
---

# 双轨接口治理专项规划

## 统一沟通语言

- 本 Prompt 产出的所有用户可见回复必须统一使用简体中文。
- 不要在正常叙述中混用英文、日文、韩文或繁体中文作为主语言。
- 代码标识符、命令、路径、字段名、报错原文，以及用户明确要求引用的原文内容，可以按原样保留。
- 需要保留非简体中文原文时，必须先给出简体中文解释，再附最小必要原文。

## 必做步骤

1. 读取 `.github/prompts/api-governance-audit.prompt.md` 的审计结论，或先按同样维度补齐审计
2. 判断涉及 `web-admin`、`flutter-app`、`shared` 哪些范围
3. 先生成治理母任务目录，例如：`tasks/api-governance-reset/`
4. 再按模块拆成子任务目录

## 使用场景

- 当用户要求对 `livehome_admin` 的管理端历史接口做成批治理、REST 化迁移、双轨梳理或治理任务拆解时，使用本 Prompt。
- 本 Prompt 不直接做业务代码实现，重点是把治理工作拆成可执行的治理任务树。

## 前置要求

开始前必须先满足两件事：

1. 已有审计结论；如果没有，就先执行 `.github/prompts/api-governance-audit.prompt.md`。
2. 已明确本轮治理针对哪些模块，而不是泛泛而谈“全部接口一起改”。

## 你的任务

你要把 API 治理改造拆成结构化任务，而不是直接产出一句口号式规划。

至少要完成：

1. 明确涉及 `web-admin`、`flutter-app`、`shared` 哪些范围。
2. 明确每个模块是保留兼容接口、直接迁移，还是进入双轨并行。
3. 为治理建立母任务目录与子任务目录。
4. 为每个模块补齐 `backend.md`、`app.md`、`web.md`、`api-contract.md` 的治理任务要求。

## 任务拆解要求

治理规划输出至少要覆盖：

- 当前接口现状
- 旧路径与新路径映射
- 生命周期状态：`primary` / `compatibility` / `deprecated`
- 权限点补齐策略
- migration_condition
- deprecation_condition
- 调用方影响范围

## 输出格式

### 1. 治理范围

- 涉及模块
- 涉及轨道：`web-admin` / `flutter-app` / `shared`
- 为什么要治理

### 2. 母任务结构

- 治理母任务目录名
- 每个子任务目录名
- 每个子任务处理的模块范围

### 3. 每模块治理策略

- 旧接口清单
- 新接口方向
- 生命周期标记
- 权限与契约补齐要求
- 前后端影响面

### 4. 产出要求

- 需要新建或更新哪些任务文件
- 哪些契约字段必须补齐
- 哪些风险必须先记录

## 关键约束

- 不要跳过审计直接生成治理规划。
- 不要把治理规划写成直接改代码指令。
- 不要把 Flutter 新接口继续规划成历史动作式路径。
- 不要遗漏 `endpoint_scope`、`lifecycle_status`、`permission_key`、`old_to_new_mapping`、`migration_condition`、`deprecation_condition`。
