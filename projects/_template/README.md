# 项目覆盖层模板

## 目录定位

- machine_readable_tag: aicopilotcb-project-overlay-template-v1
- 目录角色：新项目接入时的项目覆盖层最小样板

## 最小结构

建议至少补齐：

1. 项目说明文档
2. 项目私有规则
3. 与 `workspace-init.json`、`role-boundaries.json`、`active-context.json` 的映射说明
4. 项目专属守卫、脚本或例外约束

## 装配要求

- 不把项目私有路径、脚本和约束直接写回通用核心层。
- 若项目规则经过验证可复用，再回看是否应上移到 `core/` 或 `stacks/`。
- 项目接入前，优先使用 `tasks/_templates/project-onboarding-checklist.md` 做一次最小检查。
