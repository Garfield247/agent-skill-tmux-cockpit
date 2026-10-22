# 强类型 CLI 中枢与工兵舱生命周期 (Cockpit CLI & Lifecycle)

## 1. 强类型 All-in-One 工具中枢 (`scripts/cockpit.py`)

本技能将底层 Tmux 命令封装为 Python 3 零依赖强类型中枢脚本，**通过强类型 argv 数组原生免疫 Shell 单双引号、特殊字符与换行截断灾难**：

```bash
COCKPIT="~/.gemini/config/skills/tmux-cockpit/scripts/cockpit.py"

# 1. 外置投递至观测台 (若观测台不存在则自动切屏自愈)
$COCKPIT send "go test -v ./pkg/..."

# 2. 双向读取观测台最后 N 行日志 (直连 RCA 根因排查)
$COCKPIT capture 50

# 3. 优雅熔断卡死任务 (发送两次 SIGINT)
$COCKPIT interrupt

# 4. 状态栏高亮 Toast 交付广播
$COCKPIT toast "🚀 E2E 场景测试 16/16 全量通过" 4000

# 5. 动态派发工兵舱 (Worker Pane) 并行挂机攻坚
$COCKPIT spawn "stress-tester" "go run scripts/stress_tester/main.go -c 500"

# 6. 提取工兵产物并安全销毁窗格
$COCKPIT reap "%25" 30

# 7. 结构化 JSON 全景拓扑感知 (PID、尺寸、前台命令、活跃状态)
$COCKPIT status

# 8. 智能拓扑自愈
$COCKPIT heal
```

---

## 2. 临时工兵舱生命周期治理 (Worker Pane Lifecycle)

1. **派发原则**：多任务并行或独立压测机器人使用 `$COCKPIT spawn` 创建临时 Worker Pane；
2. **生命周期闭环**：任务执行完毕后，必须调用 `$COCKPIT reap` 安全销毁窗格，严禁遗留僵尸窗格；
3. **日志捕获门禁**：在关闭工兵舱前，必须读取产物日志并验证退出码。
