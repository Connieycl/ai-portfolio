# smolagents 与我的 tool_agent.py 五步映射表

| 我写的 tool_agent.py | smolagents 里对应什么 |
| :--- | :--- |
| **TOOLS 字典**：名字 → 函数 | **@tool 装饰器**：把带类型注解与 Args 文档的函数变成 Tool，交给 `ToolCallingAgent(tools=[...])` |
| **SYS 提示词**：要求输出 JSON | **模型原生 tool calling**：ToolCallingAgent 用模型原生 tool calling (JSON-like)，提示模板在 `prompts/toolcalling_agent.yaml` |
| **parse_calls**：剥围栏、兜底抓 JSON | **框架内部解析**：解析 `ChatMessageToolCall`，不用自己写正则 |
| **TOOLS[name](*args)**：执行 + 异常兜底 | **参数校验与调用**：框架按 `Tool.inputs` 校验参数后调用，执行结果进入多步消息 |
| **run() 手动回喂** + max_calls 收口 | **MultiStepAgent**：多步循环由框架管理步数与停止条件 |
