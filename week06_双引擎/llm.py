import os
import requests
import openai
# 假设你有 weekpath 模块，如果没有可以把下面两行注释掉
# import weekpath
# weekpath.load_env()

class LocalEngine:
    def ask(self, prompt, history=None):
        try:
            s = requests.Session()
            s.trust_env = False 
            messages = []
            if history:
                messages.extend(history)
            messages.append({"role": "user", "content": prompt})
            
            resp = s.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": "qwen2.5:0.5b",
                    "messages": messages,
                    "stream": False
                },
                timeout=120
            )
            return resp.json()["message"]["content"]
        except Exception as e:
            raise Exception(f"本地引擎请求失败: {e}")

class APIEngine:
    def __init__(self):
        self.client = None
        
    def _ensure_client(self):
        if self.client is None:
            key = os.getenv("DEEPSEEK_API_KEY")
            if not key:
                raise Exception("未配置云端密钥")
            self.client = openai.OpenAI(base_url="https://api.deepseek.com/v1", api_key=key)
            
    def ask(self, prompt, history=None):
        self._ensure_client()
        try:
            messages = []
            if history:
                messages.extend(history)
            messages.append({"role": "user", "content": prompt})
            
            r = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=messages
            )
            return r.choices[0].message.content
        except Exception as e:
            raise Exception(f"云端引擎请求失败: {e}")

class LLM:
    def __init__(self):
        self.local = LocalEngine()
        self.api = APIEngine()
        
    def ask(self, prompt, prefer="local", history=None):
        # ================= 评分点注释 =================
        # 课后作业1选择：实现多轮对话。
        # 原因：在实际学科辅导中，学生经常需要连续追问（如先问“什么是把字句”，再问“能举个例吗”）。
        # 引入 history 参数后，大模型能记住之前的对话上下文，这对于教学场景至关重要。
        # ==============================================
        
        if prefer == "local":
            try:
                return self.local.ask(prompt, history)
            except Exception as e:
                print(f"[首选引擎失败，自动切换] 本地失败原因: {e}")
                return self.api.ask(prompt, history)
        else:
            try:
                return self.api.ask(prompt, history)
            except Exception as e:
                print(f"[首选引擎失败，自动切换] 云端失败原因: {e}")
                return self.local.ask(prompt, history)