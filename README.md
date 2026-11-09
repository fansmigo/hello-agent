# Hello Agent

一个适合初学者的 Python 项目，演示“接收任务 → 选择工具 → 执行 → 返回结果”。
工具选择采用简单规则，尚未接入大模型；无需 API 密钥，无第三方依赖。

## 运行

需要 Python 3.12 或更高版本。在项目文件夹中执行：

```sh
python3.12 main.py
python3.12 main.py "现在几点？"
python3.12 main.py "统计字数：你好，Agent！"
```

若已安装 uv，也可以执行：

```sh
uv run main.py "现在几点？"
```

## 阅读代码

- `main()`：接收命令行任务。
- `run_agent()`：识别任务并调用时间或字符统计工具。

## 练习

1. 增加一个问候工具。
2. 增加一个温度换算工具。
3. 接入大模型，让模型选择工具。

## 发布到 GitHub

在 GitHub 创建一个名为 `hello-agent` 的空仓库，不勾选自动创建 README、许可证或 .gitignore。
将仓库 HTTPS 地址提供给当前聊天后，可以继续配置远程仓库和上传。
