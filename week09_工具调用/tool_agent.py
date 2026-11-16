# W9 手写最小工具调用循环（不用框架）
# 依赖：pip install openai python-dotenv
import os
import csv
import sys
import ast
import json
import re
import operator
import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weekpath  # noqa: E402  数据路径 + 加载 .env

weekpath.load_env()

import openai  # noqa: E402

VOCAB = weekpath.data_path("生词表.csv")

_client = None
_use_local = False  # 全局开关，一旦切换到本地，后续就不再尝试云端了


def get_client():
    global _client, _use_local
    if _client is None:
        if _use_local:
            _client = openai.OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
        else:
            key = os.getenv("DEEPSEEK_API_KEY")
            _client = openai.OpenAI(base_url="https://api.deepseek.com/v1", api_key=key)
    return _client


def get_time():
    return str(datetime.datetime.now())


# ---- 安全计算：白名单 AST，绝不使用裸 eval ----
_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod,
    ast.USub: operator.neg, ast.UAdd: operator.pos,
}


def _eval_node(node):
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.operand))
    raise ValueError("只允许数字与 + - * / ** % 运算")


def calc(expr):
    try:
        return str(_eval_node(ast.parse(str(expr), mode="eval")))
    except ZeroDivisionError:
        return "错误：除数为 0"
    except Exception as e:
        return "拒绝计算：%s" % e


def hsk_level(word):
    with open(VOCAB, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["词汇"].strip() == str(word).strip():
                return "%s 是 %s 级" % (word, row["HSK等级"])
    return "未找到 %s" % word


# ================= 课后作业2：新增第4个工具 =================
def evaluate_text(text):
    """课文难度评估（模拟工具）：输入课文片段，输出难度提示"""
    # 为了演示，这里简单判断字数，不进行复杂的 NLP 分词
    length = len(text)
    if length > 50:
        return f"评估结果：该课文较长（{length}字），建议作为 HSK4 阅读材料。"
    else:
        return f"评估结果：该课文较短（{length}字），建议作为 HSK3 对话材料。"
# =========================================================


# 把第4个工具注册进字典
TOOLS = {
    "get_time": get_time, 
    "calc": calc, 
    "hsk_level": hsk_level,
    "evaluate_text": evaluate_text
}

# 修改系统提示词，告诉模型多了一个工具
SYS = ("你是国际中文助教。可用工具：get_time（查时间）、calc（算术）、hsk_level（查词汇等级）、"
       "evaluate_text（评估课文难度）。"
       '如需调用，请只输出 JSON：{"tool": "工具名", "args": [参数]}；无需工具时直接回答。')


def parse_call(txt):
    s = (txt or "").strip()
    s = s.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(s)
    except Exception:
        m = re.search(r"\{.*\}", s, re.S)
        if m:
            try:
                return json.loads(m.group())
            except Exception:
                return None
    return None


def run(user_msg, max_calls=2):
    global _client, _use_local
    msgs = [{"role": "system", "content": SYS}, {"role": "user", "content": user_msg}]
    
    for _ in range(max_calls):
        model_name = "qwen2.5:0.5b" if _use_local else "deepseek-chat"
        
        try:
            txt = get_client().chat.completions.create(
                model=model_name, messages=msgs).choices[0].message.content
        except openai.APIStatusError as e:
            if "402" in str(e) or not _use_local:
                print("\n[系统提示] 云端接口请求失败(可能是余额不足)，正在自动切换至本地 Ollama...")
                _use_local = True
                _client = None
                return run(user_msg, max_calls=max_calls)
            else:
                return f"本地执行失败: {e}"
        except Exception as e:
            return f"连接失败: {e}"
            
        call = parse_call(txt)
        if not isinstance(call, dict) or call.get("tool") not in TOOLS:
            return txt
            
        args = call.get("args") or []
        if not isinstance(args, list):
            return "工具参数格式错误：%r" % (args,)
        try:
            result = TOOLS[call["tool"]](*args)
        except Exception as e:
            result = "工具执行失败：%s" % e
            
        msgs += [{"role": "assistant", "content": txt},
                 {"role": "user", "content": "工具返回：%s。请据此作答。" % result}]
    
    model_name = "qwen2.5:0.5b" if _use_local else "deepseek-chat"
    return get_client().chat.completions.create(
        model=model_name, messages=msgs).choices[0].message.content


if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "'把'字是 HSK 几级词汇？现在几点了？"
    print("用户输入：", q)
    print("助手：", run(q))