> **状态**：⏳ 待后端实现
> **功能**：{功能中文名}
> **功能目录**：`tasks/{功能英文名}/`
> **创建时间**：{日期}

---

# API 契约：{功能中文名}

> ⚠️ 前端/App **必须等待状态变为 ✅ 后再对接**

---

## 接口列表

| # | 接口名 | Method | URL | Auth | 状态 |
|---|--------|--------|-----|------|------|
| 1 | {接口名} | POST | `/api/v1/{path}` | 需要 | ⏳ |

---

## 接口详情

### 1. {接口名称}

- **URL**：`POST /api/v1/{path}`
- **Auth**：Bearer Token（需要登录）
- **说明**：{一句话描述接口用途}

#### 请求参数（Request Body）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| field_name | string | 是 | {说明} |

#### 响应示例（成功）

```json
{
  "code": 200,
  "message": "操作成功",
  "data": {}
}
```

#### 错误响应

| code | message | 触发场景 |
|------|---------|---------|
| 400 | {错误描述} | {触发条件} |
| 401 | 请先登录 | Token 无效或过期 |

---

## 数据字典

### {字段名} 枚举值

| 值 | 含义 |
|----|------|
| 0  | {含义} |
| 1  | {含义} |

---

## 前端对接注意事项

- {注意事项1}
- {注意事项2}

## 功能入口闭环信息

> 这部分用于把“接口契约”与“用户如何真正进入功能”对齐，避免只记录字段不记录使用路径。

| 项目 | 模板填写要求 |
|------|-------------|
| endpoint_scope | `web-admin` / `flutter-app` / `shared` |
| 目标用户 | 例如：后台运营、普通用户 |
| 功能入口 | 例如：左侧菜单、首页按钮、详情页跳转 |
| 页面路由 | 例如：`/admin/{module}/{name}`、`/{module}/{name}` |
| 权限 key | 如适用，填写真实权限 key |
| 依赖初始化项 | 例如：菜单数据、字典、配置、开关 |
| 最小验收路径 | 例如：登录 -> 点击入口 -> 页面加载 -> 调用接口成功 |

## 功能完成前必须确认

- [ ] 不只定义接口路径，还定义功能入口与页面路由
- [ ] 不只定义字段，还定义权限 key、依赖初始化项和验收路径
- [ ] 如果是管理端功能，菜单、路由、权限三者已经有明确映射
- [ ] 如果是 App 功能，入口、前置条件、空态或无权限态已有说明
- [ ] 前端或 App 不需要自行猜测“用户从哪里进入这个功能”

## AI 协同机器标记

```yaml
ai_collab:
  role: contract
  draft_owner: architect
  finalize_owner: backend
  consumer_roles:
    - app
    - web
  endpoint_scope_required: true
  lifecycle_status_required: true
  entrance_closure_required: true
  ready_for_consumer_when:
    - status == done
    - request_fields_completed == true
    - response_fields_completed == true
    - example_payloads_completed == true
```

- 这段骨架要求 Architect 先写草案，Backend 再把真实路径、字段和示例定稿。
- 只有契约状态真正完成后，App 和 Web 才能开始实现，不得凭经验猜接口。
