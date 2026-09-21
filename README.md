# agent-skill-tmux-cockpit

> 🚀 **Tmux 赛博战斗舱协同、外置观测投射与多 Agent 战役工兵舱 Python 强类型中枢技能**。

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Tmux](https://img.shields.io/badge/Tmux-3.0%2B-orange.svg)](https://github.com/tmux/tmux)

---

## 🌟 核心特性 (Features)

- ⚡ **纯 Python 强类型中枢 (`scripts/cockpit.py`)**：告别散装 Shell 脚本，单一文件自闭环。采用 Python 3.10+ 标准库与强类型 `dataclass`，零第三方外部依赖，具备确定性超时控制与精确退出码语义。
- 🖥️ **三联屏赛博战斗舱拓扑**：将主会话（Main Agent Pane）、左上实时观测台（Observer Pane）、左下工兵作战舱（Worker Pane）解耦，主交互对话流实现**零长篇滚屏污染 (Zero Blast Radius)**。
- 📡 **外置指令投射与非阻塞执行**：将耗时构建、全量回归测试、容器构建或服务拉起等投射至外置观测台异步执行，主会话保持毫秒级响应。
- 📸 **无头抓屏与终端视差捕获 (`capture`)**：支持毫秒级抓取目标 Pane 终端历史滚动条（支持直接输出纯文本，或调用 `alacritty`/`terminal` 截帧为 PNG），为多模态 LLM 提供客观铁证。
- 🛡️ **优雅熔断与进程回收 (`interrupt` / `reap`)**：双阶段安全熔断机制（`SIGINT` 平滑退出 ➔ 延迟升级 `SIGKILL` 强制回收），杜绝孤儿进程与僵死后台。
- 🔔 **全域状态栏与原生通知 (`toast`)**：任务交付后自动广播至 Tmux 状态栏或 macOS 原生通知中心，开发心流零打扰。
- 🩺 **环境嗅探与拓扑自愈 (`status` / `heal`)**：自动识别 `$TMUX` 宿主环境变量、探测目标 Pane 存活状态；在面板缺失时自动切分自愈。

---

## 📐 赛博战斗舱拓扑设计 (Cockpit Topology)

```text
+-------------------------------------------------------------------+
| Tmux Session: Main Workspace                                      |
+---------------------------------+---------------------------------+
| [Pane %1] AGY_OBSERVER_PANE     | [Pane %0] MAIN AGENT PANE       |
|                                 |                                 |
| 实时观测台 (Live Observer)        | 主交互上下文 (Clean Context)      |
| 耗时构建 / 测试日志 / 容器投射       | 极速决策 / 代码编写 / 方案对齐     |
| (非阻塞滚屏，主会话免受污染)        | (零滚屏刷屏，信息熵 100% 聚焦)     |
+---------------------------------+                                 |
| [Pane %2] AGY_WORKER_PANE       |                                 |
|                                 |                                 |
| 工兵作战舱 (Worker / Tooling)    |                                 |
| 多 Agent 并行沙盒 / 临时排障     |                                 |
+---------------------------------+---------------------------------+
```

---

## 🛠️ CLI 武器库全量指南 (`scripts/cockpit.py`)

所有战斗舱协同能力全量收敛至 `scripts/cockpit.py`。

### 1. 投射命令至观测台 (`send`)
```bash
# 投射全量测试至左上观测台 (默认 target=observer, 显式回车)
python3 scripts/cockpit.py send --cmd "go test -v ./..."

# 投射并覆盖执行 (向指定 pane 发送)
python3 scripts/cockpit.py send --target "%1" --cmd "npm run dev" --no-clear
```

### 2. 抓取终端输出存盘 (`capture`)
```bash
# 抓取最近 100 行日志到临时文件，供主模型切片读取
python3 scripts/cockpit.py capture --target observer --lines 100 --out /tmp/observer.log

# 捕获完整输出并输出到标准输出
python3 scripts/cockpit.py capture --target worker --lines 500
```

### 3. 优雅熔断与安全终止 (`interrupt`)
```bash
# 平滑中断观测台正在执行的任务 (SIGINT)
python3 scripts/cockpit.py interrupt --target observer

# 强力清理并杀死进程
python3 scripts/cockpit.py interrupt --target worker --force
```

### 4. 广播完成 Toast (`toast`)
```bash
# 任务完成，状态栏毫秒级广播
python3 scripts/cockpit.py toast --title "Regression Tests" --msg "128 passing (0 failures)"
```

### 5. 动态创建工兵作战舱 (`spawn`)
```bash
# 在指定窗口水平切分工兵舱
python3 scripts/cockpit.py spawn --name "worker-1" --split horizontal --size 35
```

### 6. 销毁与安全回收工兵舱 (`reap`)
```bash
# 安全回收工兵舱，释放终端资源
python3 scripts/cockpit.py reap --target "%2"
```

### 7. 环境嗅探与面板健康状态 (`status`)
```bash
# 格式化输出 Tmux 宿主环境及战斗舱拓扑状态 (支持 --json)
python3 scripts/cockpit.py status
python3 scripts/cockpit.py status --json
```

### 8. 拓扑缺失自愈 (`heal`)
```bash
# 检查观测台与工兵舱，若缺失则自动按标准三联屏拓扑切分并导出环境变量
python3 scripts/cockpit.py heal
```

---

## 📦 安装与多 Agent 使用指南 (Installation & Multi-Agent Usage)

### 1. Google Antigravity / Gemini Code Assist
- **全局安装（推荐）**：
  ```bash
  git clone git@github.com:Garfield247/agent-skill-tmux-cockpit.git ~/.gemini/config/skills/tmux-cockpit
  ```
- **项目工作区局部引入**：
  ```bash
  mkdir -p .agents/skills
  git clone git@github.com:Garfield247/agent-skill-tmux-cockpit.git .agents/skills/tmux-cockpit
  ```

### 2. Anthropic Claude (Claude Code / Claude Projects)
- **Claude Code (CLI 终端智能体)**：
  ```bash
  mkdir -p ~/.claude/skills
  git clone git@github.com:Garfield247/agent-skill-tmux-cockpit.git ~/.claude/skills/tmux-cockpit
  ```
- **Claude Projects (Web 客户端)**：
  直接将仓库中的 `SKILL.md` 内容复制并粘贴至 Project 的 **Project Knowledge**。

### 3. Cursor / GitHub Copilot / OpenAI Codex
- **Cursor (现代 MDC 规则体系)**：
  ```bash
  mkdir -p .cursor/rules
  git clone git@github.com:Garfield247/agent-skill-tmux-cockpit.git .cursor/rules/tmux-cockpit
  ```
- **GitHub Copilot / Codex**：
  将 `SKILL.md` 放置于工作区 `.github/copilot-instructions.md` 或直接作为系统提示词导入。

---

## 📄 开源许可证 (License)

本项目采用 [MIT License](LICENSE) 授权许可。
