# W4 命令行学科问答机器人（完整免安装版）
import os
import json
import urllib.request

# ================= 1. 密钥配置 =================
# 请将下面的密钥替换为你自己的真实密钥
DEEPSEEK_API_KEY = "sk-c4b905d8f3dd466091aa6e7ad1c17103"

# ================= 2. 基础配置 =================
BASE_URL = "https://api.deepseek.com/v1/chat/completions"
MODEL = "deepseek-chat"

# ================= 3. 核心请求函数 =================
def ask(question, temperature=0.7, max_tokens=800):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": question}],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    req = urllib.request.Request(
        BASE_URL, 
        data=json.dumps(data).encode('utf-8'), 
        headers=headers, 
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['choices'][0]['message']['content']
    except Exception as e:
        return f"请求出错: {e}"

# ================= 4. 运行主程序 =================
if __name__ == "__main__":
    
    # ---------- 第2步：跑通3个专业问题（生成日志） ----------
    questions = [
        "把字句的教学难点有哪些",
        "HSK4级对词汇量的要求是多少",
        "给一篇中级汉语作文写三段式评语"
    ]
    
    log_file = "chat_log.txt"
    print("开始运行，正在请求AI...\n")
    
    with open(log_file, "a", encoding="utf-8") as f:
        for q in questions:
            print(f"正在问：{q}")
            ans = ask(q)
            print(f"AI回答：{ans[:50]}...")
            f.write("Q: %s\nA: %s\n\n" % (q, ans))
            print("-" * 40)
            
    print(f"\n日志已保存到 {log_file}")

    # ---------- 第3步：参数体验（对应讲义评分点） ----------
    print("\n" + "="*40)
    print("开始参数体验实验（对比 temperature 和 max_tokens）")
    print("="*40)
    
    test_q = "用一句话说明什么是把字句"
    
    print("\n【实验1：temperature = 0.0】（看结果是否稳定）")
    ans1 = ask(test_q, temperature=0.0)
    print(ans1)
    
    print("\n【实验2：temperature = 1.5】（看结果是否发散）")
    ans2 = ask(test_q, temperature=1.5)
    print(ans2)
    
    print("\n【实验3：max_tokens = 15】（看是否被截断）")
    ans3 = ask(test_q, max_tokens=15)
    print(ans3)
    
    print("\n【实验4：max_tokens = 800】（看完整回答）")
    ans4 = ask(test_q, max_tokens=800)
    print(ans4)
    
    print("\n所有实验完成！")
    