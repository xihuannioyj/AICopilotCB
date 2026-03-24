# stacks

这个目录用于承载按技术栈划分的协同适配规则。

当前已经建立的技术栈子目录如下：

- stacks/java/
- stacks/python/
- stacks/go/
- stacks/android/
- stacks/ios/
- stacks/angular/
- stacks/flutter/
- stacks/wechat-miniapp/
- stacks/douyin-miniapp/

每个技术栈目录只负责沉淀该技术栈通用的工程约束，不直接承载某个项目自己的业务规则。

建议每个子目录后续至少继续沉淀三类内容：

- 构建与运行约束
- 测试与验证约束
- 该技术栈常见的协同边界与交接规则
