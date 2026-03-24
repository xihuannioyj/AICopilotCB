# android

## 技术栈定位

- 适用范围：原生 Android App、Android SDK、混合栈中的 Android 端实现
- 继承关系：默认继承 `core/` 的任务闭环、回流协议和收尾模板

## 推荐读取顺序

1. 先读 `core/README.md`
2. 再读 `docs/requirements/02-技术栈适配层.md`
3. 最后结合项目覆盖层确认模块结构、构建变体和设备验证路径

## 最小入口

- 构建入口：优先识别 `build.gradle`、`settings.gradle`、`gradlew`
- 运行入口：优先识别 Application/Launcher Activity 与本地安装脚本
- 测试入口：优先识别 `test/`、`androidTest/` 与 lint/assemble 相关任务

## 常见角色组合

- architect + android + backend
- android + test-collector + defect-triage

## 常见风险与交接

- 需确认 minSdk、targetSdk、构建变体和签名策略
- 原生插件、权限、推送、支付、摄像头等问题不得用 Web 结论替代
- 交接时要写清真机验证范围、平台限制和仍依赖服务端的能力
