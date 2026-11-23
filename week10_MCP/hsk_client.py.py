import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_DIR = r"C:\Connie\华文小助手_代码骨架\week10_MCP"
PYTHON     = r"E:\python\python.exe"
SERVER     = SERVER_DIR + r"\hsk_mcp_server.py"

async def main():
    server = StdioServerParameters(
        command=PYTHON,
        args=[SERVER],
        cwd=SERVER_DIR,
    )
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print("工具列表:", [t.name for t in tools.tools])
            res = await session.call_tool("hsk_level", {"word": "把"})
            print("调用结果:", res.content[0].text)

asyncio.run(main())