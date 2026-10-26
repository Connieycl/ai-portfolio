from llm import LLM

bot = LLM()

print("=== 开始测试 ===")
# 强制本地，如果本地挂了就会自动切云端
ans = bot.ask("什么是把字句？", prefer="local")
print("最终拿到的答案：", ans)