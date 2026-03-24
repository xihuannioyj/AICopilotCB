# java

## 技术栈定位

- 适用范围：Java 服务端、Spring Boot 项目、工具型 Java 工程
- 继承关系：默认继承 `core/` 的任务闭环、回流协议和收尾模板

## 推荐读取顺序

1. 先读 `core/README.md`
2. 再读 `docs/requirements/02-技术栈适配层.md`
3. 最后结合具体项目的 `projects/{project-name}/` 覆盖层补差异

## 最小入口

- 构建入口：优先识别 `pom.xml`、`build.gradle`、`gradlew`
- 运行入口：优先识别 Spring Boot 主启动类或项目 README 中的本地启动脚本
- 测试入口：优先识别 `src/test/`、Maven/Gradle test 任务与项目级验证脚本

## 常见角色组合

- architect + backend + doc-manager
- backend + test-collector + defect-triage

## 常见风险与交接

- 需提前确认 JDK 版本、构建工具和多模块结构
- 若涉及数据库迁移、配置文件或环境变量，应在 handoff 中显式说明
- 若项目同时包含 Web/Admin 轨道，应把对外契约与内部实现分开说明
