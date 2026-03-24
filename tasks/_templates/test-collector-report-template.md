# 测试收集工程师缺陷采集模板

机器标记：
- role_template: test-collector
- output_type: issue-collection
- handoff_to: defect-triage

## 1. 测试范围

- 功能名称：{feature-name}
- 页面入口：{entry-route}
- 测试端：{angular-or-flutter-web}
- 运行地址：{local-url}
- 预期行为：{expected-behavior}

## 2. 缺陷清单

- 缺陷编号：{issue-id}
- 页面 / 组件：{page-or-component}
- 现象描述：{symptom}
- 复现步骤：{steps}
- 实际结果：{actual-result}
- 预期结果：{expected-result}
- 严重级别建议：{severity}

## 3. 证据

- 命令控制台错误：{terminal-errors}
- VS Browser 控制台错误：{browser-console-errors}
- 接口异常：{network-errors}
- 截图 / 录屏引用：{screenshots}
- 备注：{notes}

## 4. 交接说明

- 建议交给角色：{suggested-owner}
- 是否阻断验收：{blocking-flag}
- 是否需要 defect-triage 进一步归因：{need-triage}
