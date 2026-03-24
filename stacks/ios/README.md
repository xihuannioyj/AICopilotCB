# ios

## 技术栈定位

- 适用范围：原生 iOS App、iOS SDK、混合栈中的 iOS 端实现
- 继承关系：默认继承 `core/` 的任务闭环、回流协议和收尾模板

## 推荐读取顺序

1. 先读 `core/README.md`
2. 再读 `docs/requirements/02-技术栈适配层.md`
3. 最后结合项目覆盖层确认工程结构、签名和设备验证路径

## 最小入口

- 构建入口：优先识别 `Package.swift`、`Podfile`、`*.xcodeproj`、`*.xcworkspace`
- 运行入口：优先识别 App target、Scheme 与本地模拟器/真机启动方式
- 测试入口：优先识别单元测试 Target、UI 测试 Target 与项目级验证脚本

## 常见角色组合

- architect + ios + backend
- ios + test-collector + defect-triage

## 常见风险与交接

- 需确认签名、证书、Scheme、模拟器与真机差异
- 原生权限、支付、推送、相机、定位等问题必须单独标记平台限制
- 交接时要写清验证设备范围、构建前置条件和仍依赖服务端的能力
