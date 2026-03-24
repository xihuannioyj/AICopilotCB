# 缺陷分诊模板

机器标记：
- role_template: defect-triage
- output_type: triage-decision
- handoff_to: backend|app|web|product-manager|doc-manager

## 1. 缺陷来源

- 来源任务：{source-task}
- 来源角色：{source-role}
- 缺陷编号：{issue-id}
- 证据链接：{evidence-links}

## 2. 分诊结论

- 归因类型：{backend|app|web|product|docs|environment}
- 责任角色：{owner-role}
- 优先级：{priority}
- 是否阻断：{blocking-flag}
- 根因判断置信度：{confidence}

## 3. 回流动作

- 建议动作：{recommended-action}
- 回流目标任务：{returned-task}
- 是否需要补契约：{need-contract-update}
- 是否需要产品澄清：{need-pm-clarification}
- 是否需要文档经理同步：{need-doc-sync}

## 4. 备注

- 对开发的说明：{engineering-notes}
- 对测试复测的说明：{retest-notes}
- 对 Owner 的风险提示：{owner-risk-summary}
