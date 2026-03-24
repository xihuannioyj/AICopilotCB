# python

## 技术栈定位

- 适用范围：Python 脚本型项目、服务型项目、自动化控制面脚本
- 继承关系：默认继承 `core/` 的任务闭环、回流协议和收尾模板

## 推荐读取顺序

1. 先读 `core/README.md`
2. 再读 `docs/requirements/02-技术栈适配层.md`
3. 最后结合项目覆盖层确认虚拟环境、依赖与运行脚本

## 最小入口

- 构建入口：优先识别 `requirements.txt`、`pyproject.toml`、`setup.py`
- 运行入口：优先识别主脚本、CLI 入口或项目 README 中的启动命令
- 测试入口：优先识别 `tests/`、`pytest.ini`、`tox.ini` 或项目级验证脚本

## 常见角色组合

- architect + backend + doc-manager
- aicopilotcb-evolution + doc-manager + test-collector

## 常见风险与交接

- 需先确认虚拟环境、依赖锁定方式和本地解释器版本
- 脚本型项目与服务型项目的校验链不同，handoff 中必须显式说明
- 若涉及迁移、定时任务或数据脚本，应单独标记可回滚方式
