"""一个使用规则选择工具的 Agent 入门演示，不调用大模型。"""

import argparse
from datetime import datetime
from zoneinfo import ZoneInfo

from weather import get_weather


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
        tool = "城市天气工具"
        city = task.strip()
        for prefix in ("查询天气", "查天气", "天气", "weather"):
            if city.lower().startswith(prefix):
                city = city[len(prefix):].lstrip(" ：:")
                break
        else:
            if city.endswith("天气"):
                city = city[:-2].rstrip(" 的")
        result = get_weather(city)
    return f"选择工具：{tool}\n执行结果：{result}"


def main() -> None:
    parser = argparse.ArgumentParser(description="零依赖 Agent 工具调用演示")
    parser.add_argument("task", nargs="?", default="现在几点？")
    parser.add_argument("--city", help="直接指定要查询天气的城市，例如：上海")
    args = parser.parse_args()
    if args.city is not None:
        print(f"任务：查询城市天气：{args.city}")
        print(f"选择工具：城市天气工具\n执行结果：{get_weather(args.city)}")
    else:
        print(f"任务：{args.task}")
        print(run_agent(args.task))


if __name__ == "__main__":
    main()
