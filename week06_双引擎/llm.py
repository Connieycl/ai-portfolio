import os
import requests
import openai
# import weekpath  # 如果有这个包就保留，没有就删掉
# weekpath.load_env()

class LocalEngine:
    def ask(self, prompt):
        try:
            s = requests.Session()
            s.trust_env = False 
            resp = s.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": "qwen2.5:0.5b",
                    "messages": [{"role": "user", "content": prompt}],
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
            
    def ask(self, prompt):
        self._ensure_client()
        try:
            r = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}]
            )
            return r.choices[0].message.content
        except Exception as e:
            raise Exception(f"云端引擎请求失败: {e}")

class LLM:
    def __init__(self):
        self.local = LocalEngine()
        self.api = APIEngine()
        
    def ask(self, prompt, prefer="local"):
        # 这就是异常回退逻辑
        if prefer == "local":
            try:
                return self.local.ask(prompt)
            except Exception as e:
                print(f"本地失败，自动回退云端: {e}")
                return self.api.ask(prompt)
        else:
            try:
                return self.api.ask(prompt)
            except Exception as e:
                print(f"云端失败，自动回退本地: {e}")
                return self.local.ask(prompt)