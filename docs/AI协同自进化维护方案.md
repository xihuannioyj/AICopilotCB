# AI协同自进化维护方案

## 文档定位

- machine_readable_tag: aicopilotcb-self-evolution-plan-v1
- 文档角色：说明 AICopilotCB 如何以治理模式持续维护自身控制面

## 核心原则

1. 先收敛重复规则，再新增新规则。
2. 先补稳定载体，再扩展流程表达。
3. 优先把路径、边界、项目实例等易变信息下沉到配置真源。
4. 所有方案级写入都必须通过 guard 校验。

## 演进循环

1. 发现规则冲突、断链引用、缺失模板或重复口径。
2. 判断问题属于 core、stacks、projects、prompts、agents、runtime 还是 docs。
3. 做最小修改并补齐稳定载体。
4. 更新 `docs/AI协同方案进度.md` 与 `docs/使用说明书.md`。
5. 运行单文件与全量 guard 校验。

## 非目标

- 不把业务代码修复伪装成控制面演进。
- 不把未验证经验直接提升为全局硬规则。
