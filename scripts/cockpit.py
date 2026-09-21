#!/usr/bin/env python3
"""
cockpit.py: 赛博战斗舱 All-in-One 强类型中枢 CLI (零依赖 Python 3 标准库)
集成外置投射、双向读回、安全熔断、状态栏广播、多 Agent 工兵派发与声明式拓扑自愈。
"""

import argparse
import json
import os
import subprocess
import sys
import time


def run_tmux(args, check=True):
    """底层安全调用 tmux，参数为强类型数组，天然免疫 Shell 引号转义翻车"""
    try:
        res = subprocess.run(
            ["tmux"] + args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=check,
        )
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        return None
    except FileNotFoundError:
        print("❌ 未找到 tmux 命令，请确认宿主环境已安装 tmux", file=sys.stderr)
        return None


def is_in_tmux():
    return bool(os.environ.get("TMUX"))


def get_observer_pane(ensure=False):
    """获取观测台 Pane ID，如果不存在且指定 ensure=True 则自动自愈切出"""
    if not is_in_tmux():
        return None

    obs = run_tmux(["show-environment", "AGY_OBSERVER_PANE"], check=False)
    obs_id = obs.split("=", 1)[1] if obs and "=" in obs else None

    # 校验该 pane 是否仍然存活
    panes_raw = run_tmux(["list-panes", "-F", "#{pane_id}"], check=False) or ""
    alive_panes = panes_raw.splitlines()

    if obs_id and obs_id in alive_panes:
        return obs_id

    if not ensure:
        return None

    # 自动自愈：在当前窗口上方切出 35% 空间作为观测台
    new_obs = run_tmux(["split-window", "-v", "-b", "-p", "35", "-P", "-F", "#{pane_id}"])
    if new_obs:
        run_tmux(["set-environment", "AGY_OBSERVER_PANE", new_obs])
        # 将焦点切回主舱
        run_tmux(["last-pane"], check=False)
        return new_obs
    return None


def cmd_send(args):
    """外置投递指令至左上观测台 (原生免转义)"""
    if not is_in_tmux():
        print("⚠️  [cockpit] 当前不在 Tmux 宿主环境中，降级为直接执行:")
        subprocess.run(args.command, shell=True)
        return

    obs = get_observer_pane(ensure=True)
    if not obs:
        print("❌ [cockpit] 无法定位或初始化观测台", file=sys.stderr)
        sys.exit(1)

    # 通过强类型 argv 直接投递，天然避免单双引号截断
    run_tmux(["send-keys", "-t", obs, args.command, "C-m"])
    print(f"🚀 [cockpit] 任务已投射至左上观测台 ({obs}): {args.command}")


def cmd_capture(args):
    """双向读取观测台最后 N 行日志输出"""
    if not is_in_tmux():
        print("⚠️  [cockpit] 当前不在 Tmux 环境中")
        return

    obs = get_observer_pane(ensure=False)
    if not obs:
        print("⚠️  [cockpit] 观测台当前未在线")
        return

    output = run_tmux(["capture-pane", "-p", "-t", obs, "-S", f"-{args.lines}"], check=False)
    if output is not None:
        print(output)


def cmd_interrupt(args):
    """向观测台发送 SIGINT (Ctrl+C) 优雅熔断卡死任务"""
    if not is_in_tmux():
        return

    obs = get_observer_pane(ensure=False)
    if not obs:
        print("⚠️  [cockpit] 观测台未在线")
        return

    run_tmux(["send-keys", "-t", obs, "C-c"])
    time.sleep(0.15)
    run_tmux(["send-keys", "-t", obs, "C-c"])
    print(f"🛑 [cockpit] 已向观测台 ({obs}) 发送中断信号 (Ctrl+C)")


def cmd_toast(args):
    """向 Tmux 底部状态栏发送高亮完成通知"""
    if not is_in_tmux():
        print(args.message)
        return

    run_tmux(["display-message", "-d", str(args.duration), args.message], check=False)


def cmd_spawn(args):
    """动态切出独立工兵舱 (Worker Pane) 并指派任务 (标杆 2: 黑板协同)"""
    if not is_in_tmux():
        print("⚠️  [cockpit] 当前不在 Tmux 环境中，降级为后台进程执行")
        subprocess.Popen(args.command, shell=True)
        return

    worker_pane = run_tmux(["split-window", "-v", "-p", "35", "-c", os.getcwd(), "-P", "-F", "#{pane_id}"])
    if not worker_pane:
        print("❌ [cockpit] 创建工兵舱失败", file=sys.stderr)
        sys.exit(1)

    run_tmux(["select-pane", "-t", worker_pane, "-T", f"Worker: {args.name}"])
    run_tmux(["send-keys", "-t", worker_pane, args.command, "C-m"])
    run_tmux(["last-pane"], check=False)
    print(f"🚀 [工兵派发成功] 标识: {args.name} | 窗格 ID: {worker_pane}")


def cmd_reap(args):
    """回收工兵舱：提取最后产物日志并安全销毁窗格"""
    if not is_in_tmux():
        return

    pane_id = args.pane_id
    panes_raw = run_tmux(["list-panes", "-F", "#{pane_id}"], check=False) or ""
    if pane_id not in panes_raw.splitlines():
        print(f"ℹ️  工兵窗格 ({pane_id}) 已结束或已被回收")
        return

    print(f"=== [工兵舱 {pane_id} 产出日志 (最后 {args.lines} 行)] ===")
    out = run_tmux(["capture-pane", "-p", "-t", pane_id, "-S", f"-{args.lines}"], check=False)
    if out:
        print(out)
    print("=================================================")

    run_tmux(["kill-pane", "-t", pane_id], check=False)
    print(f"🧹 [工兵舱 {pane_id} 已安全销毁回收]")


def cmd_status(args):
    """输出当前战斗舱完整拓扑全景 JSON (标杆 3: 强类型结构化状态)"""
    if not is_in_tmux():
        print(json.dumps({"in_tmux": False, "error": "Not in a tmux session"}))
        return

    session = run_tmux(["display-message", "-p", "#{session_name}"])
    fmt = "#{pane_id}|#{pane_index}|#{pane_width}|#{pane_height}|#{pane_active}|#{pane_current_command}|#{pane_current_path}|#{pane_pid}"
    raw = run_tmux(["list-panes", "-F", fmt]) or ""

    panes = []
    for line in raw.splitlines():
        parts = line.split("|")
        if len(parts) >= 8:
            panes.append({
                "pane_id": parts[0],
                "index": int(parts[1]),
                "width": int(parts[2]),
                "height": int(parts[3]),
                "is_active": parts[4] == "1",
                "command": parts[5],
                "path": parts[6],
                "pid": int(parts[7]),
            })

    obs_pane = get_observer_pane(ensure=False)
    res = {
        "in_tmux": True,
        "session": session,
        "total_panes": len(panes),
        "observer_pane": obs_pane,
        "observer_alive": any(p["pane_id"] == obs_pane for p in panes) if obs_pane else False,
        "panes": panes,
    }
    print(json.dumps(res, indent=2, ensure_ascii=False))


def cmd_heal(args):
    """智能拓扑自愈：秒级校验并恢复观测台"""
    if not is_in_tmux():
        print("⚠️  当前不在 tmux 环境中，跳过自愈")
        return

    obs = get_observer_pane(ensure=True)
    print(f"✅ [自愈中枢] 战斗舱拓扑健康，观测台已就绪: {obs}")


def main():
    parser = argparse.ArgumentParser(
        description="cockpit: 赛博战斗舱 All-in-One 强类型中枢 CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="action", required=True)

    # 1. send
    p_send = sub.add_parser("send", help="外置投递指令至左上观测台")
    p_send.add_argument("command", help="待执行的完整命令字符串")
    p_send.set_defaults(func=cmd_send)

    # 2. capture
    p_cap = sub.add_parser("capture", help="双向读取观测台屏幕输出")
    p_cap.add_argument("lines", nargs="?", type=int, default=30, help="抓取行数 (默认 30)")
    p_cap.set_defaults(func=cmd_capture)

    # 3. interrupt
    p_int = sub.add_parser("interrupt", help="向观测台发送 SIGINT 优雅熔断任务")
    p_int.set_defaults(func=cmd_interrupt)

    # 4. toast
    p_toast = sub.add_parser("toast", help="向状态栏发送完成广播通知")
    p_toast.add_argument("message", help="广播消息内容")
    p_toast.add_argument("duration", nargs="?", type=int, default=4000, help="展示毫秒数 (默认 4000)")
    p_toast.set_defaults(func=cmd_toast)

    # 5. spawn
    p_spawn = sub.add_parser("spawn", help="动态派发独立工兵舱 (Worker)")
    p_spawn.add_argument("name", help="工兵任务标识名")
    p_spawn.add_argument("command", help="工兵执行命令")
    p_spawn.set_defaults(func=cmd_spawn)

    # 6. reap
    p_reap = sub.add_parser("reap", help="回收工兵舱资源并销毁窗格")
    p_reap.add_argument("pane_id", help="工兵窗格 ID (如 %25)")
    p_reap.add_argument("lines", nargs="?", type=int, default=30, help="提取尾部日志行数")
    p_reap.set_defaults(func=cmd_reap)

    # 7. status
    p_stat = sub.add_parser("status", help="获取当前战斗舱全景 JSON 状态")
    p_stat.set_defaults(func=cmd_status)

    # 8. heal
    p_heal = sub.add_parser("heal", help="智能自愈观测台拓扑")
    p_heal.set_defaults(func=cmd_heal)

    parsed = parser.parse_args()
    parsed.func(parsed)


if __name__ == "__main__":
    main()
