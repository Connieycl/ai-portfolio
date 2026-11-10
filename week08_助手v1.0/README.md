# 学科智能问答助手 v1.0

## 功能
- 基于 RAG 的学科问答；支持纯对话 / 基于资料两种模式，具备双向引擎回退机制。

## 怎么装
- 推荐环境：Python 3.12
- pip install -r requirements.txt
- 复制 .env.example 为 .env，填入 DEEPSEEK_API_KEY
- 确保本地已安装 Ollama，并执行：ollama pull qwen2.5:0.5b 及 ollama pull nomic-embed-text

## 怎么用
- python assistant_v1.py（从 week08_助手v1.0 目录运行）

## 已知问题
- 本机存在严重显卡驱动冲突（CUDA error），本地运行可能会崩溃，建议在终端执行 `set OLLAMA_NO_CUDA=1` 强制使用 CPU 模式。
- 云端备用接口若余额不足（Error 402），会触发异常兜底，程序不会闪退。
