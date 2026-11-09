"""一个使用规则选择工具的 Agent 入门演示，不调用大模型。"""

import argparse
from datetime import datetime
from zoneinfo import ZoneInfo


def run_agent(task: str) -> str:
    if any(word in task.lower() for word in ("时间", "几点", "time")):
        tool = "北京时间工具"
        result = datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S")
    elif any(word in task.lower() for word in ("字数", "统计", "count")):
        tool = "字符统计工具"
        _, separator, content = task.partition(":")
        if not separator:
            _, separator, content = task.partition("：")
        if not separator:
            return "请使用格式：统计字数：你好，Agent！"
        result = f"共有 {len(content.strip())} 个字符（包含标点和内部空格）。"
    else:
        return "我可以查询时间或统计字数。试试：现在几点？ / 统计字数：你好，Agent！"
    return f"选择工具：{tool}\n执行结果：{result}"


def main() -> None:
    parser = argparse.ArgumentParser(description="零依赖 Agent 工具调用演示")
    parser.add_argument("task", nargs="?", default="现在几点？")
    args = parser.parse_args()
    print(f"任务：{args.task}")
    print(run_agent(args.task))


if __name__ == "__main__":
    main()
