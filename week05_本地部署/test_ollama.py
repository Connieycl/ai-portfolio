import requests

s = requests.Session()
# 机房有代理时必须加，否则连不上本机
s.trust_env = False 

resp = s.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "qwen2.5:0.5b",
        "messages": [{"role": "user", "content": "给《愚公移山》出一道HSK4阅读题"}],
        "stream": False
    },
    timeout=120
)

print(resp.json()["message"]["content"])