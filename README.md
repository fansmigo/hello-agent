# Hello Agent

一个适合初学者的 Python 项目，演示“接收任务 → 选择工具 → 执行 → 返回结果”。
工具选择采用简单规则，尚未接入大模型；无需 API 密钥，无第三方依赖。

## 运行

需要 Python 3.12 或更高版本。在项目文件夹中执行：

```sh
python3.12 main.py
python3.12 main.py "现在几点？"
python3.12 main.py "统计字数：你好，Agent！"
python3.12 main.py "北京"
python3.12 main.py "天气：上海"
python3.12 main.py "北京天气"
python3.12 main.py --city "London"
```

若已安装 uv，也可以执行：

```sh
uv run main.py "现在几点？"
uv run main.py --city "上海"
```

## 城市天气查询

输入城市名称，Agent 会调用天气工具：先查询城市的经纬度，再查询当前天气，
显示匹配地区、当地数据时间、天气、温度、体感温度、湿度和风速。
只输入“天气”会提示补充城市。原有时间和字数工具继续可用。

天气查询需要联网，使用 [Open-Meteo 天气 API](https://open-meteo.com/en/docs)
和[城市搜索 API](https://open-meteo.com/en/docs/geocoding-api)，个人非商业练习无需密钥。
当前天气为模型估算，非气象站实测。城市搜索采用第一个匹配结果，请核对输出地区；
遇到同名城市可尝试 `--city "Paris, France"`，中文找不到时可尝试拼音或英文。
连接超时、城市不存在和服务数据异常都会返回中文提示。

## 在 VS Code 中运行

1. 在 VS Code 打开此项目文件夹，安装 Microsoft 的 Python 和 Python Debugger 扩展。
2. 通过“Python: Select Interpreter”选择项目的 `.venv/bin/python`，或其他 Python 3.12+ 解释器。
3. 打开“运行和调试”，选择“查询城市天气”，按 F5，输入城市后回车。
4. 在下方集成终端查看天气结果。也可以直接在终端运行上面的命令。

## 测试

```sh
.venv/bin/python -m unittest -v
```

测试模拟网络响应，覆盖城市解析、天气输出、网络异常和原有工具，不需要联网。

## 阅读代码

- `main()`：接收命令行任务。
- `run_agent()`：识别任务并调用时间、字符统计或城市天气工具。
- `weather.py` 的 `get_weather()`：城市定位、天气查询和错误处理。
- `.vscode/launch.json`：输入城市并启动调试。

## 练习

1. 增加一个问候工具。
2. 增加一个温度换算工具。
3. 接入大模型，让模型选择工具。

## 发布到 GitHub

在 GitHub 创建一个名为 `hello-agent` 的空仓库，不勾选自动创建 README、许可证或 .gitignore。
将仓库 HTTPS 地址提供给当前聊天后，可以继续配置远程仓库和上传。
