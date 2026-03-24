# 8 Agent 协作起手 Prompt

## 使用场景

- 当你希望按 8 Agent 团队启动一个新需求、体验优化或缺陷治理任务时，优先使用本 Prompt。
- 适用于：先让产品经理补全需求、识别缺陷和不合理项、给出行业/竞品改进建议并完善开发计划，再让 architect 拆任务，随后由 backend / app / web 执行，最后接 tester / test-collector / defect-triage / doc-manager 收口。

## 默认调用顺序

1. `product-manager`：先做需求补全、用户路径梳理、缺口识别、不合理项判断、竞品参考、体验目标和开发计划建议。
2. `architect`：再产出 `backend.md`、`app.md`、`web.md`、`api-contract.md`。
3. `backend`：先定稿真实契约并实现接口。
4. `flutter` / `angular`：按契约并行开发。
5. `tester`：继续承担当前最小回流闭环。
6. `test-collector`：在页面可联调后采集控制台错误、UI 和交互问题。
7. `defect-triage`：把采集结果转成优先级、责任归属和回流建议。
8. `doc-manager`：统一更新说明书、日报、进度和文档收口。

## 当前阶段限制

- 当前立即启用：`product-manager`、`doc-manager`。
- 当前协议占位，升级后激活：`test-collector`、`defect-triage`。
- 如果当前任务只涉及协同方案维护，默认仍然只修改 `.github/`、`docs/`、`指南.md`。

## 推荐输入模板

请按 8 Agent 团队流程处理这个需求：先让 `product-manager` 补全需求短板，识别不合理项与隐藏依赖，结合行业/竞品给出改进建议，并完善开发计划与验收口径；再让 `architect` 按分析结果拆出 `backend.md`、`app.md`、`web.md`、`api-contract.md`。如果需要联调和缺陷闭环，再按 `backend -> flutter/angular -> tester -> test-collector -> defect-triage -> doc-manager` 的顺序推进，不要跳步骤，也不要让前端先猜接口。

## 直接可用示例

### 示例 1：新功能起手

请先用 `product-manager` 深入分析这个功能的目标用户、核心场景、需求短板、不合理诉求、竞品参考、体验要求、阶段划分和验收口径，再把结果交给 `architect` 拆成 backend / app / web / api-contract 四份任务文档。

### 示例 2：页面联调与问题收集

这个功能的 Angular 页面和 Flutter Web 页面已经能打开了。请先按契约完成联调，再让 `test-collector` 收集命令控制台错误、VS Browser 控制台错误、UI 样式问题和交互问题，最后交给 `defect-triage` 做归因和回流建议。

### 示例 3：文档收口

请让 `doc-manager` 基于当前任务状态、运行态报表和角色输出，统一更新说明书、日报、阶段进度和剩余风险，不要改业务代码。
