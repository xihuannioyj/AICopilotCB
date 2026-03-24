# stacks

## 目录定位

- machine_readable_tag: aicopilotcb-stacks-readme-v1
- 目录角色：承载各技术栈在协同执行面上的最小适配骨架

## 继承关系

- `stacks/` 继承 `core/` 的角色边界、回流协议、收尾模板和写入校验规则。
- `stacks/` 只补充构建、运行、测试、联调与交接差异，不重新定义通用核心层协议。

## 当前技术栈目录

- stacks/java/
- stacks/python/
- stacks/go/
- stacks/android/
- stacks/ios/
- stacks/angular/
- stacks/flutter/
- stacks/wechat-miniapp/
- stacks/douyin-miniapp/

## 每个技术栈目录的最小要求

每个 `stacks/{tech}/` 至少应说明：

1. 技术栈定位与适用范围
2. 推荐读取顺序
3. 构建、运行、测试的最小入口
4. 常见协作角色组合
5. 常见风险点与交接方式

## 维护原则

- 技术栈适配层只沉淀技术差异，不承载单项目目录和脚本私货。
- 某个技术栈规则若未经过至少一个项目样板验证，只保留最小骨架，不做过度细化。
- 某条规则一旦被两个以上项目复用，再评估是否继续上移到 `core/`。
