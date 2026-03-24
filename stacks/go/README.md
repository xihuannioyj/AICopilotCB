# go

## 技术栈定位

- 适用范围：Go 服务、CLI 工具、单仓多模块 Go 项目
- 继承关系：默认继承 `core/` 的任务闭环、回流协议和收尾模板

## 推荐读取顺序

1. 先读 `core/README.md`
2. 再读 `docs/requirements/02-技术栈适配层.md`
3. 最后结合项目覆盖层确认模块布局与本地运行方式

## 最小入口

- 构建入口：优先识别 `go.mod`、`Makefile`、项目脚本入口
- 运行入口：优先识别主包、服务启动脚本或 README 中的本地启动方法
- 测试入口：优先识别 `go test` 相关目录、测试包和 lint 脚本

## 常见角色组合

- architect + backend + doc-manager
- backend + test-collector + defect-triage

## 常见风险与交接

- 需确认模块边界、生成代码流程和环境变量依赖
- 若使用多二进制入口或多服务目录，handoff 中必须写清启动入口
- 若存在平台差异构建，应在验证步骤中先收敛到最小可运行目标
