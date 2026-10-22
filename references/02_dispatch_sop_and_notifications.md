# 调度投射 SOP、广播与审查舱联动 (Dispatch SOP & Notifications)

## 1. 核心调度与投射协议 (Dispatch SOP)

### 1.1 宿主感知与观测台嗅探
在执行耗时超过 5 秒的构建、测试、压测或长跑服务前，按序探测：
```bash
if [ -n "$TMUX" ]; then
    OBS_PANE=$(tmux show-environment AGY_OBSERVER_PANE 2>/dev/null | cut -d= -f2)
fi
```

### 1.2 外置投射场景分支
- **场景 A：命中三联屏环境（`$OBS_PANE` 存在）**：
  - 强制优先投射：使用 `tmux send-keys -t "$OBS_PANE" "<cmd>" C-m`；
  - 主会话轻量回显：仅输出一句提示，绝不长篇滚屏；
- **场景 B：普通单窗格 Tmux 环境（无 `$OBS_PANE`）**：
  - 使用纵向切屏：`tmux split-window -v -p 35 "<cmd>"` 临时切出独立监控窗格；
- **场景 C：非 Tmux 纯终端环境**：
  - 降级为后台任务调度或管道截流（`> /tmp/run.log 2>&1`），仅向主会话汇报退出码与关键摘要。

---

## 2. 状态栏广播协议 (Toast Notification)

对于运行时间较长的后台任务（全量回归、基准测试、自动化压测、/goal 攻坚完成）：
- **必须调用 Tmux 原生状态栏广播**：
  ```bash
  tmux display-message -d 4000 "🚀 [agy 交付通知] <简明完成摘要，如：E2E 场景自动化测试 16/16 全量通过>"
  ```
- 确保用户即使切走视线或在另一个窗格打字，也能在底部状态栏第一时间捕获交付信号。

---

## 3. 可视化审查舱联动 (Git Diff Review)

当用户需要多文件大范围审阅 git diff 时：
- 主动调用系统命令切出 `lazygit` 交互审查舱：
  ```bash
  tmux split-window -h -p 50 "lazygit"
  ```
- 免去用户手动切屏敲命令的摩擦，审阅完毕直接按 `q` 退出自动恢复原布局。
