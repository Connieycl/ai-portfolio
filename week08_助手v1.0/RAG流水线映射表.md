# 官方 RAG 流水线 ↔ 我的 rag_qa.py：5 行映射表

1. **Load + Split**：官方 Document loader + Text splitter -> 我的 TextLoader + RecursiveCharacterTextSplitter(500/50)。
2. **Embed + Store**：官方 Embeddings 与 VectorStore -> 我的 OllamaEmbeddings / OpenAIEmbeddings + Chroma。
3. **Retrieve**：官方 2-Step RAG 检索总在生成之前 -> 我的 retrieve() 取 top-k。
4. **Prompt + Generate**：官方检索片段拼 prompt 再给 LLM -> 我的 build_prompt() 拼接 SYSTEM_HINT 与资料。
5. **Deploy + Evaluate**：官方 Streamlit 部署与系统评估 -> 我的 W7 幻觉对照表评估。
