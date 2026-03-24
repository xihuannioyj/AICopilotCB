# flutter

## 技术栈定位

- 适用范围：Flutter App、Flutter Web、跨端客户端项目
- 继承关系：默认继承 `core/` 的任务闭环、回流协议和收尾模板

## 推荐读取顺序

1. 先读 `core/README.md`
2. 再读 `docs/requirements/02-技术栈适配层.md`
3. 最后结合项目覆盖层确认路由、状态管理、联调环境和平台差异

## 最小入口

- 构建入口：优先识别 `pubspec.yaml`
- 运行入口：优先识别 `lib/` 主入口、Web 启动方式或真机调试方式
- 测试入口：优先识别 `test/`、Widget/Integration 测试脚本和项目级验证脚本

## 常见角色组合

- architect + flutter + backend
- flutter + test-collector + defect-triage

## 常见风险与交接

- 需先确认平台目标是移动端、Web 还是桌面端
- 联调阶段必须区分 mock 与真实接口
- 交接时要写清页面范围、路由注册、仍依赖后端的数据或权限项
