import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weekpath  # noqa: E402  数据路径 + 加载 .env

weekpath.load_env()

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# 文件路径定位
CORPUS = weekpath.data_path("等级标准节选.txt")
PERSIST = weekpath.root_path("chroma_db")

_retriever = None

def get_retriever(k=3, rebuild=False):
    global _retriever
    if _retriever is not None and not rebuild:
        return _retriever
        
    # 核心：使用云端 API 做向量化，彻底摆脱本地显卡依赖
    emb = OpenAIEmbeddings(
        model="deepseek-chat", 
        base_url="https://api.deepseek.com/v1",
        api_key=os.getenv("DEEPSEEK_API_KEY") 
    )
    
    if not rebuild and os.path.exists(PERSIST) and os.listdir(PERSIST):
        vs = Chroma(persist_directory=PERSIST, embedding_function=emb)
    else:
        docs = TextLoader(CORPUS, encoding="utf-8").load()
        splits = RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=50).split_documents(docs)
        vs = Chroma.from_documents(splits, emb, persist_directory=PERSIST)
    _retriever = vs.as_retriever(search_kwargs={"k": k})
    return _retriever

def retrieve(question):
    return "\n".join(d.page_content for d in get_retriever().invoke(question))

def build_prompt(question, ctx):
    return ("根据以下资料回答问题，资料中没有的内容就如实说“资料中未提及”：\n"
            "%s\n\n问题：%s" % (ctx, question))

if __name__ == "__main__":
    from llm import LLM          # week06 的模块

    llm = LLM()
    
    # 课后作业1（方案B）：支持多轮追问
    history = []
    print("=== 已开启多轮对话模式（输入 'quit' 退出） ===")
    
    while True:
        q = input("\n你: ")
        if q.lower() == 'quit':
            break
            
        print("【正在检索资料并生成答案...】")
        try:
            ctx = retrieve(q)
            print("【检索片段】\n", ctx[:300], "\n---")
            
            # 强制使用云端 API 生成，不走本地
            ans = llm.ask(build_prompt(q, ctx), prefer="api", history=history)
            print("AI:", ans)
            
            history.append({"role": "user", "content": q})
            history.append({"role": "assistant", "content": ans})
        except Exception as e:
            print("出错了:", e)