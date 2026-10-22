---
name: tmux-cockpit
description: >-
  Tmux 终端多路复用协同、赛博三联屏战斗舱拓扑治理、宿主感知、左上观测台外置投射、
  长耗时测试与微服务后台监控、Toast 状态栏广播及交互审查舱调度工程规范技能。
---

# Tmux 赛博战斗舱协同与外置观测工程规范 (Tmux Cockpit Skill)

## 核心协同铁律 (Core Redlines)
1. 🚨 **严禁在主交互舱跑长滚屏命令**：测试日志超过 50 行或常驻服务，严禁在主会话直接运行导致记忆与屏幕雪崩；
2. 🚨 **严禁篡改用户主刀区**：左下角用户工作区严禁通过 `send-keys` 注入任何未经许可的内容；
3. 🚨 **必须提供命令退出码与铁证收口**：投射至观测台的任务，在主会话中声称“完成”前，必须读取日志并确认退出码；
4. 🚨 **优雅自愈原则**：若投递时观测台已失效，自动调用 `$COCKPIT heal` 重建补位，绝不报错卡死；
5. 🚨 **工兵舱生命周期自闭环**：通过 `$COCKPIT spawn` 派发的临时工兵舱，任务结束必须调用 `$COCKPIT reap` 安全回收。

## 标准协同工作流 (Workflow SOP)
1. **宿主环境感知**：探测 `$TMUX` 与 `AGY_OBSERVER_PANE`，识别战斗舱拓扑；
2. **外置命令投射**：耗时构建、回归测试或常驻服务，通过 `cockpit.py send` 投射至左上角观测台；
3. **主会话轻量回显**：主对话流仅输出一句状态提示，保持架构思维与决策心流；
4. **铁证捕获与状态广播**：执行完毕调用 `cockpit.py capture` 验证退出码，并触发 `cockpit.py toast` 状态栏广播。

## 渐进式参考手册索引 (Progressive Disclosure References)
更深入的拓扑规划、投射协议与 Python CLI 脚本说明，按需调阅：

| 领域模块 | 子手册路径 | 核心覆盖内容 |
| :--- | :--- | :--- |
| **三联屏拓扑与窗格职能** | [01_cockpit_topology_and_roles.md](file:///Users/garfield/.gemini/config/skills/tmux-cockpit/references/01_cockpit_topology_and_roles.md) | 赛博三联屏黄金布局、主舱/观测台/用户区三大窗格职能与环境变量 |
| **调度投射与通知广播** | [02_dispatch_sop_and_notifications.md](file:///Users/garfield/.gemini/config/skills/tmux-cockpit/references/02_dispatch_sop_and_notifications.md) | 宿主感知嗅探、外置投射场景分支、Tmux 原生 Toast 状态栏广播、lazygit 审查舱联动 |
| **强类型 CLI 中枢与生命周期** | [03_cockpit_cli_and_lifecycle.md](file:///Users/garfield/.gemini/config/skills/tmux-cockpit/references/03_cockpit_cli_and_lifecycle.md) | `scripts/cockpit.py` 强类型命令矩阵 (send/capture/toast/spawn/reap)、工兵舱生命周期 |
