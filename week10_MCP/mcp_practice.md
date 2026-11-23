# W10 MCP 实验报告

## 一、配置记录
- **运行环境**：使用绝对路径的 Python 解释器，确保环境一致。路径为 E:\python\python.exe
- **服务端启动**：在 week10_MCP 目录下运行 python hsk_mcp_server.py，服务端成功启动并进入 stdio 监听状态（挂起等待连接）。
- **客户端配置**：使用 Python 编写的 hsk_client.py 客户端脚本，通过 StdioServerParameters 指定服务端路径和运行目录，拉起了服务端进程进行通信。
- **配置原文**：{"mcpServers": {"hsk-tools": {"command": "python", "args": ["hsk_mcp_server.py"]}}}

## 二、调用证据
- **工具列表输出**：['hsk_level', 'list_by_level']
- **实际调用结果**：把 -> 3 级

*(注：已在终端中成功复现上述结果，证明 MCP 协议握手与工具调用链路完全打通。)*

## 三、三者辨析
1. **Function Calling（模型侧机制）**：大模型自身的核心能力，负责决定“我要调哪个工具”，输出意图和参数。
2. **MCP（工具侧协议）**：把各种外部工具统一封装，解决“工具怎么被标准化发现和调用”的问题，像 USB 接口一样通用。
3. **普通 API 调用（程序侧直连）**：传统的网络请求方式，程序员硬编码直接请求特定接口，没有大模型决策的参与。
