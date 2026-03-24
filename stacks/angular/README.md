# angular

## 技术栈定位

- 适用范围：Angular Web 管理端、门户端、控制台类前端项目
- 继承关系：默认继承 `core/` 的任务闭环、回流协议和收尾模板

## 推荐读取顺序

1. 先读 `core/README.md`
2. 再读 `docs/requirements/02-技术栈适配层.md`
3. 最后结合项目覆盖层确认前端路由、接口轨道与本地联调约束

## 最小入口

- 构建入口：优先识别 `package.json`、`angular.json`
- 运行入口：优先识别本地 dev server 脚本和路由入口
- 测试入口：优先识别 `src/` 测试目录、lint/test 脚本和页面验收路径

## 常见角色组合

- architect + angular + backend
- angular + test-collector + defect-triage

## 常见风险与交接

- 需先确认路由入口、页面可达路径、菜单依赖和权限依赖
- 接口消费前必须确认真实契约，不得靠页面猜字段
- 交接时要写清已接入路由、页面范围、阻塞字段和空态/无权限态处理
