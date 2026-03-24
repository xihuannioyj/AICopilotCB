# wechat-miniapp

## 技术栈定位

- 适用范围：微信小程序项目及其配套协同规则
- 继承关系：默认继承 `core/` 的任务闭环、回流协议和收尾模板

## 推荐读取顺序

1. 先读 `core/README.md`
2. 再读 `docs/requirements/02-技术栈适配层.md`
3. 最后结合项目覆盖层确认分包结构、平台能力和提审要求

## 最小入口

- 构建入口：优先识别 `project.config.json`、`app.json` 和开发者工具配置
- 运行入口：优先识别页面入口、分包入口与本地调试路径
- 测试入口：优先识别页面验证路径、接口联调路径与提审前检查项

## 常见角色组合

- architect + frontend/app + backend
- test-collector + defect-triage + backend

## 常见风险与交接

- 需确认授权、支付、分享和平台能力的开通条件
- 开发者工具中的本地调试结果不等于提审结果
- 交接时要写清页面入口、分包归属和平台能力依赖
