import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weekpath
weekpath.load_env()

from llm import LLM
from rag_qa import retrieve, build_prompt

# 设置系统提示词
SYSTEM_HINT = "你是国际中文教学助手，面向 HSK3-4 学习者，回答需给出依据。"

# 实例化 LLM 对象（之前你漏了这句导致报错）
llm = LLM()

def answer(question, use_rag=True, prefer="local"):
    if use_rag:
        ctx = retrieve(question)
        prompt = SYSTEM_HINT + "\n" + build_prompt(question, ctx)
    else:
        prompt = SYSTEM_HINT + "\n" + question
        
    return llm.ask(prompt, prefer=prefer)

if __name__ == "__main__":
    questions = [
        "把字句的教学难点有哪些",
        "HSK4 词汇量要求是多少",
        "《愚公移山》可以设计什么课堂活动"
    ]
    
    print("=== 助手 v1.0 启动 (纯本地CPU模式) ===")
    for q in questions:
        print(f"\nQ: {q}")
        try:
            # 核心：强制走本地，且对返回结果做二次防崩溃处理
            ans = answer(q, prefer="local")
            print(f"A: {ans}")
        except Exception as e:
            # 如果底层 Ollama 还是因为显卡或内存报错，这里直接拦截并友好提示
            print(f"A: [运行失败] 底层引擎报错。原因：{str(e)}")
        print("-" * 40)