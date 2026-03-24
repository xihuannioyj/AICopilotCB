> **分配给**：Angular AI 工程师（管理后台 Web 端）
> **功能**：{功能中文名}
> **状态**：⬜ 等待 api-contract.md 完成后开始
> **依赖**：`api-contract.md` 状态必须为 ✅ 才可开始

---

# Web 任务：{功能中文名}

## 零、职责边界与依赖声明

- 当前任务默认由 `angular` 承担页面、前端路由、页面级按钮入口、渲染和接口消费。
- Angular 不负责菜单表落库、权限点入库、seed 数据和接口字段定稿。
- 若页面访问依赖服务端菜单、权限或测试数据，必须在本任务中显式标记为 backend 依赖项。

## 零点一、入口闭环与阻塞声明

| 项目 | 内容 | 责任人 | 当前状态 |
|------|------|--------|---------|
| 前端路由 | {route_path} | angular | ⬜ |
| 页面按钮或菜单入口 | {按钮/菜单说明} | angular | ⬜ |
| 服务端菜单初始化 | {是否需要 backend 落库} | backend | ⬜ |
| 权限与测试数据依赖 | {权限 key / 测试账号 / seed} | backend | ⬜ |

## 零点二、收尾交接要求

- 收尾时必须写清：已接入路由、已完成页面范围、仍依赖 backend 的菜单/权限/测试数据项、下一棒是谁。
- 页面已完成但入口闭环未完成时，只能标记 Web 部分完成，不能把整个功能标记为 done。

## 一、页面清单

| 页面名 | 路由 | 组件路径 |
|--------|------|---------|
| {页面名}管理 | `/admin/{module}/{name}` | `src/app/pages/admin/{module}/{name}/` |

---

## 二、列表页设计

### 搜索条件

| 字段 | 类型 | 说明 |
|------|------|------|
| keyword | 文本输入 | 关键词搜索 |
| status | 下拉选择 | 状态筛选 |

### 表格列定义

| 列名 | 字段 | 类型 | 宽度 | 说明 |
|------|------|------|------|------|
| ID | id | number | 80px | |
| {列名} | {field} | string | {width} | {说明} |
| 状态 | status | tag | 100px | 0=待处理 1=已完成 |
| 创建时间 | created_at | datetime | 160px | |
| 操作 | - | - | 120px | 编辑/删除 |

---

## 三、新增/编辑弹窗表单

| 字段名 | 控件类型 | 必填 | 验证规则 | 说明 |
|--------|---------|------|---------|------|
| {field} | Input | 是 | required | {说明} |

---

## 四、API 调用清单

| # | 接口用途 | Service 方法 | 调用时机 |
|---|---------|-------------|---------|
| 1 | 获取列表 | `{Name}Service.list()` | 页面初始化/搜索/换页 |
| 2 | 新增 | `{Name}Service.create()` | 弹窗提交 |
| 3 | 编辑 | `{Name}Service.update()` | 弹窗提交 |
| 4 | 删除 | `{Name}Service.delete()` | 确认后 |

**Service 文件**：`src/app/services/{name}.service.ts`

---

## 五、TypeScript 类型定义

**文件**：`src/app/models/{name}.model.ts`

```typescript
export interface {Name}Model {
  id: number;
  {field}: {type};
  status: number;
  created_at: string;
}
```

---

## 六、权限要求

| 操作 | 所需权限 slug |
|------|-------------|
| 查看列表 | `{module}.list` |
| 新增 | `{module}.create` |
| 编辑 | `{module}.update` |
| 删除 | `{module}.delete` |

---

## 七、任务清单

- [ ] 等待后端更新 `api-contract.md` 为 ✅
- [ ] 创建 TypeScript 接口定义
- [ ] 创建 Service（list/create/update/delete）
- [ ] 创建模块文件
- [ ] 创建组件文件（.ts/.html/.less）
- [ ] 实现搜索表单
- [ ] 实现 NzTable（含分页）
- [ ] 实现新增/编辑弹窗（含表单验证）
- [ ] 实现删除确认（NzPopconfirm）
- [ ] 添加路由（懒加载）
- [ ] 浏览器测试通过

## 六、入口闭环清单

| 项目 | 模板填写要求 |
|------|-------------|
| 目标用户 | 例如：后台运营、管理员、审核员 |
| 进入入口 | 例如：左侧菜单、列表页按钮、详情页跳转 |
| 页面路由 | 例如：`/admin/{module}/{name}` |
| 菜单挂载位置 | 例如：挂到“{一级菜单} / {二级菜单}”下 |
| 权限 key | 例如：`admin.{module}.{resource}.index` |
| 依赖初始化项 | 例如：菜单数据、字典、配置项、默认筛选项 |
| 最小验收路径 | 例如：登录后台 -> 点击菜单 -> 进入页面 -> 数据加载成功 |

> 这部分不是可选补充项。凡是管理端页面任务，都必须填写，避免页面文件存在但用户无入口进入。

## 七、菜单与路由落地任务

- [ ] 注册页面路由
- [ ] 挂载菜单或补齐按钮跳转入口
- [ ] 对齐权限 key、菜单可见性和接口权限控制
- [ ] 如依赖初始化菜单/字典/配置，补齐对应落地方式
- [ ] 验证“登录 -> 入口 -> 页面 -> 数据加载或关键操作成功”最小链路

## AI 协同机器标记

```yaml
ai_collab:
  role: web
  task_kind: consumer-implementation
  contract_source: tasks/{功能英文名}/api-contract.md
  start_condition: api-contract.status == done
  entrance_closure_required: true
  menu_binding_required: true
  permission_alignment_required: true
  route_registration_required: true
  allowed_write_roots:
    - livehome_ng/src/
    - livehome_ng/public/
    - livehome_ng/package.json
    - livehome_ng/angular.json
  forbidden_write_roots:
    - livehome_app/
    - livehome_admin/
```

- 这段骨架要求 Angular 任务默认输出菜单、路由、权限三者的一致性。
- 如果页面文件已写但菜单入口和权限映射仍为空，该任务不能视为完成。
- 如果实际改动路径超出 `allowed_write_roots`，必须回退给 architect 或 owner 重新拆任务，不要跨目录顺手改。
