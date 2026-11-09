# 学科智能问答助手 v1.0

## 功能
- 基于 RAG 的学科问答；支持纯对话 / 基于资料两种模式。

## 怎么装
- pip install -r requirements.txt
- 复制 .env.example 为 .env，填入 DEEPSEEK_API_KEY

## 怎么用
- python assistant_v1.py（从 week08_助手v1.0 目录运行）

## 已知问题
- **本地环境限制**：本机 RTX 3050 显卡驱动与 Ollama 存在底层冲突，运行本地推理（Embedding与生成）时会触发 CUDA error 崩溃。
- **云端限制**：若无余额，云端 API 会返回 402 错误。建议配置好云端环境后，强制指定 `prefer="api"` 运行。
