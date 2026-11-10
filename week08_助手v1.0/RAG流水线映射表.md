# 官方 RAG 流水线 ↔ 我的 rag_qa.py 5行映射表

1. **Load + Split**：官方用 Document loader + Text splitter；我用 TextLoader + RecursiveCharacterTextSplitter(500/50) 读取 HSK 资料。
2. **Embed + Store**：官方默认云端 Embeddings；我将其替换为本地隐私安全的 OllamaEmbeddings(nomic-embed-text) 并存入 Chroma。
3. **Retrieve**：官方 2-Step RAG 检索在先；我的代码由 retrieve() 提取 Top-K，use_rag=True 时控制先查资料。
4. **Prompt + Generate**：官方将片段拼入 Prompt；我的代码由 build_prompt() 拼接提示词，交由本地 LLM().ask() 生成。
5. **Deploy + Evaluate**：官方用 Streamlit 部署；我的代码用命令行组装，并用 W7 幻觉对照表完成评估。
