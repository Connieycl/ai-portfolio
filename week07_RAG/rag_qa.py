import os
import sys
import weekpath

# 加载环境变量（虽然本地跑不需要真密钥，但代码里要有）
weekpath.load_env()

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# 文件路径定位
CORPUS = weekpath.data_path("等级标准节选.txt")
PERSIST = weekpath.root_path("chroma_db")

_retriever = None

def get_retriever(k=3, rebuild=False):
    global _retriever
    if _retriever is not None and not rebuild:
        return _retriever
        
    # 【核心修改】强制使用本地 Ollama 进行向量化
    emb = OllamaEmbeddings(model="nomic-embed-text")
    
    if not rebuild and os.path.exists(PERSIST) and os.listdir(PERSIST):
        vs = Chroma(persist_directory=PERSIST, embedding_function=emb)
    else:
        docs = TextLoader(CORPUS, encoding="utf-8").load()
        splits = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents(docs)
        vs = Chroma.from_documents(splits, emb, persist_directory=PERSIST)
        
    _retriever = vs.as_retriever(search_kwargs={"k": k})
    return _retriever

def retrieve(question):
    try:
        docs = get_retriever().invoke(question)
        return "\n".join(d.page_content for d in docs)
    except Exception as e:
        print(f"[检索阶段警告]: {e}")
        return "未找到相关资料"

def build_prompt(question, ctx):
    return ("根据以下资料回答问题，资料中没有的内容就如实说“资料中未提及”：\n"
            "%s\n\n问题：%s" % (ctx, question))