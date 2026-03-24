> **分配给**：后端 AI 工程师（Laravel/PHP）
> **功能**：{功能中文名}
> **状态**：⬜ 未开始
> **创建时间**：{日期}
> **依赖**：无（后端先行）

---

# 后端任务：{功能中文名}

## 零、职责边界与交接前提

- 当前任务默认由 `backend` 承担接口契约定稿、表结构调整、migration、seed、菜单数据初始化、权限点、联调样例数据等职责。
- 若该功能支撑管理端页面，必须补齐“菜单入口如何落库、权限 key 如何初始化、测试数据如何提供”。
- 本任务完成后，backend 交给 angular 或 flutter 的内容必须显式写清：真实路由、请求字段、响应字段、错误码、测试数据状态、是否仍缺菜单或权限初始化。

## 零点一、入口闭环清单

| 项目 | 内容 | 责任人 | 当前状态 |
|------|------|--------|---------|
| 页面或功能入口 | {菜单/按钮/跳转入口} | architect/backend | ⬜ |
| 权限 key | {permission_key} | backend | ⬜ |
| 初始化方式 | {migration/seed/脚本/后台初始化} | backend | ⬜ |
| 联调样例数据 | {测试账号/seed/示例响应} | backend | ⬜ |

## 一、数据库设计

### 新增表：`{table_name}`

```sql
CREATE TABLE `{table_name}` (
  `id`         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id`    BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
  `field_name` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '{说明}',
  `status`     TINYINT NOT NULL DEFAULT 0 COMMENT '状态 0=xx 1=xx',
  `created_at` TIMESTAMP NULL,
  `updated_at` TIMESTAMP NULL,
  `deleted_at` TIMESTAMP NULL COMMENT '软删除',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='{表说明}';
```

---

## 二、API 实现任务

### API 1：{接口名称} `{METHOD} /api/v1/{path}`

**路由文件**：`routes/api.php`

#### Controller（`app/Http/Controllers/V1/API/{Name}Controller.php`）

- `{methodName}(Request $request)`：参数验证 → 调用 Service → 返回 success

#### Service（`app/Services/{Name}Service.php`）

逻辑步骤：

1. {步骤1}
2. {步骤2}
3. 如果 {条件}，抛出 BusinessException('{错误信息}', 400)
4. 返回 {返回数据说明}

#### Repository（`app/Repository/{Name}Repository.php`）

```sh
{queryMethod}(int $userId): ?Model
{saveMethod}(array $data): Model
```

---

## 三、业务逻辑流程

```ini
用户请求 → 参数验证 → Service
  成功 → 更新状态 → 返回结果
  失败 → 抛出异常（code=400）
```

---

## 四、边界条件与异常处理

| 情况 | 处理方式 | 返回 |
|------|---------|------|
| {条件1} | {处理} | code=400, message={消息} |
| 数据库写入失败 | 事务回滚 | code=500 |

---

## 五、依赖关系

- 依赖 Service：{如 CoinService::addCoin()}
- 依赖 Model：{如 User}

---

## 六、任务清单

- [ ] 创建 Migration 文件
- [ ] 执行迁移
- [ ] 创建/更新 Model
- [ ] 创建 Repository 方法
- [ ] 创建 Service 逻辑
- [ ] 创建 Controller 方法
- [ ] 注册路由
- [ ] **更新 `api-contract.md` 状态为 ✅（前端等待此步骤）**
- [ ] 本地接口测试通过

## 八、管理端入口配套项

如果该功能支撑 `livehome_ng` 管理端页面，后端任务不能只交付接口，还必须明确以下配套项：

| 项目 | 模板填写要求 |
|------|-------------|
| 管理端入口用途 | 例如：列表页、详情页、审核页、报表页 |
| 权限 key | 例如：`admin.{module}.{resource}.index` |
| 菜单数据来源 | 例如：后台菜单表、初始化 Seeder、迁移脚本、人工初始化 |
| 初始化方式 | 例如：Seeder、SQL、后台菜单维护、配置项 |
| 依赖字典/配置 | 例如：状态字典、筛选项、开关配置 |
| 验收支持 | 说明后台登录后如何通过菜单/路由进入页面并命中当前接口 |

> 如果缺少权限 key、菜单数据、初始化方式或验收支持说明，则该后端任务不能算真正支撑了管理端可用功能。

## 九、入口闭环相关任务

- [ ] 明确管理端权限 key
- [ ] 明确菜单数据或初始化落地方式
- [ ] 明确页面进入后依赖的字典/配置接口
- [ ] 确认接口权限控制与页面入口权限一致
- [ ] 支持最小验收链路：登录 -> 入口 -> 页面 -> 接口返回成功

## AI 协同机器标记

```yaml
ai_collab:
  role: backend
  task_kind: implementation
  contract_source: tasks/{功能英文名}/api-contract.md
  contract_finalize_required: true
  entrance_closure_required: true
  approval_gate: manual-if-contract-or-cross-system-risk
  allowed_write_roots:
    - livehome_admin/app/
    - livehome_admin/routes/
    - livehome_admin/tests/
    - livehome_admin/database/
    - livehome_admin/config/
  forbidden_write_roots:
    - livehome_ng/
    - livehome_app/
  assisted_execution:
    default: denied
    allowed_only_when:
      - taskMode == assisted-implementation
      - manualApproval.status == approved
      - validationsResult.overall != failed
    safe_write_scope:
      - livehome_admin/app/
      - livehome_admin/routes/
      - livehome_admin/tests/
```

- Architect 必须先把这段骨架补齐，Backend 再根据真实实现定稿。
- 普通 implementation 任务不得把自己描述成可直接 assisted-execution。
- 如果实际改动路径超出 `allowed_write_roots`，必须回退给 architect 或 owner 重新拆任务，不要跨目录顺手改。
