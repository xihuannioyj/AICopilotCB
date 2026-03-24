# projects/livehome

这个目录用于承载 LiveHome 项目的覆盖层规则。

凡是仍然直接依赖以下内容的，都优先归到这里：

- livehome_admin/、livehome_app/、livehome_ng/ 的目录边界
- tasks/ 的任务板、派发索引和运行态约束
- LiveHome 特有的 API 规范、权限 key、菜单初始化和入口闭环规则
- 只对当前 LiveHome 研发流程成立的 Prompt、Agent 约束或守卫要求

通用化拆分时，默认先把 LiveHome 专属约束留在这里，再逐步识别哪些部分可以继续上移到 core/ 或 stacks/。
