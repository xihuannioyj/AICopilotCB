> **分配给**：Flutter AI 工程师（移动端 App）
> **功能**：{功能中文名}
> **状态**：⬜ 等待 api-contract.md 完成后开始
> **依赖**：`api-contract.md` 状态必须为 ✅ 才可开始

---

# App 任务：{功能中文名}

## 零、职责边界与依赖声明

- 当前任务默认由 `flutter` 承担 App 页面、客户端路由、模型、状态和接口消费。
- Flutter 不负责数据库种子数据、菜单或权限初始化、接口字段定稿。
- 若当前阶段使用本地 mock 占位，必须显式记录，不能把 mock 结果当作真实契约完成。

## 零点一、入口闭环与阻塞声明

| 项目 | 内容 | 责任人 | 当前状态 |
|------|------|--------|---------|
| 客户端路由 | {route_name} | flutter | ⬜ |
| 页面入口方式 | {tab/按钮/列表项/启动页} | flutter | ⬜ |
| 服务端数据依赖 | {接口/测试数据/权限限制} | backend | ⬜ |
| 本地 mock 状态 | {是否仍在使用} | flutter | ⬜ |

## 零点二、收尾交接要求

- 收尾时必须写清：已完成页面、已注册路由、仍依赖 backend 的字段/数据/权限项、是否仍存在本地 mock。
- 真实接口未联通或关键依赖未完成时，只能标记 App 部分完成，不能把整个功能标记为 done。

## 一、页面清单

| 页面名 | 文件路径 | 入口方式 |
|--------|---------|---------|
| {页面名} | `lib/pages/{module}/{name}_page.dart` | {路由名/弹窗} |

---

## 二、页面 UI 设计

### {页面名}

**布局结构**：

```ini
Scaffold
  AppBar（title: {标题}）
  Body（SafeArea）
    {组件1描述}
    {组件2描述}
    底部操作按钮：{按钮文字}
```

**核心交互**：

1. 进入页面时：{初始化行为}
2. 点击{按钮}时：{触发逻辑}
3. 成功时：{显示提示 / 跳转页面}
4. 失败时：{显示错误信息}

---

## 三、状态管理（BLoC）

__BLoC 文件__：`lib/blocs/{module}/{name}_bloc.dart`

**Events**：

- `Load{Name}` — {触发时机}
- `Do{Action}` — {触发时机}

**States**：

- `{Name}Initial`
- `{Name}Loading`
- `{Name}Loaded(data)`
- `{Name}Success`
- `{Name}Failure(message)`

---

## 四、API 调用清单

> 字段名以 `api-contract.md` 为最终准

| # | 接口用途 | Service 方法 | 调用时机 |
|---|---------|-------------|---------|
| 1 | {用途} | `{Service}.{method}()` | {时机} |

__Service 文件__：`lib/services/{name}_service.dart`

---

## 五、Model 定义

__文件__：`lib/models/{name}_model.dart`

```ini
{ModelName} {
  字段1: {类型} — {说明}
  字段2: {类型} — {说明}
}
需要实现：fromJson 工厂方法
```

---

## 六、本地缓存策略

| 数据 | 缓存时长 | Hive Box | Key |
|------|---------|---------|-----|
| {数据名} | {时长} | {box_name} | {key} |

---

## 七、任务清单

- [ ] 等待后端更新 `api-contract.md` 为 ✅
- [ ] 创建 Model 类（含 fromJson）
- [ ] 创建/更新 Service 方法
- [ ] 创建 BLoC（Events / States / Bloc）
- [ ] 创建页面文件
- [ ] 实现 UI 布局
- [ ] 接入 BLoC 状态
- [ ] 实现本地缓存逻辑
- [ ] 注册路由
- [ ] 添加国际化文本（app_zh.arb）
- [ ] 真机/模拟器测试通过

## 六、页面可达性清单

| 项目 | 模板填写要求 |
|------|-------------|
| 目标用户 | 例如：普通用户、已登录用户、经纪人 |
| 进入入口 | 例如：首页按钮、个人中心、消息跳转、弹窗入口 |
| 页面路由 | 例如：`/{module}/{name}` |
| 前置条件 | 例如：必须登录、必须实名认证、必须有某状态数据 |
| 空态/无权限态 | 例如：无数据提示、无权限提示、引导跳转 |
| 最小验收路径 | 例如：登录 App -> 点击“{入口名}” -> 进入页面 -> 数据加载或操作成功 |

> 这部分用于避免 App 页面只有代码实现，没有真实用户进入路径。

## 七、入口与跳转任务

- [ ] 注册页面路由
- [ ] 补齐真实入口或跳转链路
- [ ] 明确登录态、实名态或其他前置条件
- [ ] 补齐空态、异常态、无权限态
- [ ] 验证最小链路：登录 -> 入口 -> 页面 -> 数据加载或关键操作成功

## AI 协同机器标记

```yaml
ai_collab:
  role: app
  task_kind: consumer-implementation
  contract_source: tasks/{功能英文名}/api-contract.md
  start_condition: api-contract.status == done
  entrance_closure_required: true
  route_registration_required: true
  empty_state_required: true
  permission_state_required: true
  allowed_write_roots:
    - livehome_app/lib/
    - livehome_app/test/
    - livehome_app/web/
    - livehome_app/pubspec.yaml
  forbidden_write_roots:
    - livehome_ng/
    - livehome_admin/
```

- 这段骨架用于提醒 Flutter 任务只能消费已经定稿的契约，不能反向猜接口。
- 如果入口、前置条件、空态或无权限态没填，说明任务还没到可稳定交付状态。
- 如果实际改动路径超出 `allowed_write_roots`，必须回退给 architect 或 owner 重新拆任务，不要跨目录顺手改。
