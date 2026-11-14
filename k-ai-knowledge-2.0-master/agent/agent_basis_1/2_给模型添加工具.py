from langchain_community.chat_models import ChatTongyi
from langchain.tools import tool
from langchain.messages import ToolMessage

# 1.创建模型客户端
llm = ChatTongyi(model="qwen3-max")


# 2.给 LLM 添加工具
@tool
def get_weather(location: str) -> str:
    """
    获取某个位置的天气信息
    :param location: 地理位置
    :return: 天气情况
    """
    return f"{location}的天气是100摄氏度，请你准备防晒。"


# 2.2.将工具绑定到 LLM
tools = [get_weather]
model_with_tools = llm.bind_tools(tools=tools)

# 3.调用模型
user_input = "明天北京的天气怎么样？"
# user_input = "波士顿和东京的天气怎么样？"
messages = [
    ("system", "你是一个友好的天气查询助手"),
    ("human", f"{user_input}")
]

result = model_with_tools.invoke(messages)
print(type(result))  # <class 'langchain_core.messages.ai.AIMessage'>
print(result)
"""
{
  "content": "",
  "additional_kwargs": {
    "tool_calls": [
      {
        "function": {
          "arguments": "{\"location\": \"北京\"}",
          "name": "get_weather"
        },
        "id": "call_4cca4f03f0f149878644f727",
        "index": 0,
        "type": "function"
      }
    ]
  },
  "response_metadata": {
    "model_name": "qwen3-max",
    "finish_reason": "tool_calls",
    "request_id": "82419405-acf9-9a5d-b281-35f55537cc25",
    "token_usage": {
      "input_tokens": 282,
      "output_tokens": 21,
      "prompt_tokens_details": {
        "cached_tokens": 0
      },
      "total_tokens": 303
    }
  },
  "id": "lc_run--019f0c50-62e0-7351-9913-40c15f074e8c-0",
  "tool_calls": [
    {
      "name": "get_weather",
      "args": {
        "location": "北京"
      },
      "id": "call_4cca4f03f0f149878644f727",
      "type": "tool_call"
    }
  ],
  "invalid_tool_calls": []
}
"""

# 4. 根据 tool_calls 调用工具
tool_map = {tool.name: tool for tool in tools}

if result.tool_calls:
    # 关键步骤：将 AI 的响应添加到消息历史中
    messages.append(result)

    for tool_call in result.tool_calls:
        tool_name = tool_call.get("name")
        tool_args = tool_call.get("args", {})
        tool_id = tool_call.get("id")

        tool_func = tool_map.get(tool_name)

        if tool_func:
            try:
                tool_result = tool_func.invoke(tool_args)
                print(f"调用工具 '{tool_name}' 成功，结果: {tool_result}")

                # 创建 ToolMessage 并将结果添加到消息历史
                tool_message = ToolMessage(
                    content=tool_result,
                    tool_call_id=tool_id
                )
                messages.append(tool_message)

            except Exception as e:
                print(f"调用工具 '{tool_name}' 失败: {e}")
                tool_message = ToolMessage(
                    content=f"工具调用失败: {str(e)}",
                    tool_call_id=tool_id
                )
                messages.append(tool_message)
        else:
            print(f"未找到工具: {tool_name}")
            tool_message = ToolMessage(
                content=f"未找到工具: {tool_name}",
                tool_call_id=tool_id
            )
            messages.append(tool_message)
else:
    print("没有需要调用的工具")
    print(result.content)

# 5. 再次调用模型，获取最终回答
print("\n" + "=" * 50)
print("消息历史:")
for msg in messages:
    print(f"{type(msg).__name__}: {msg}")
print("=" * 50 + "\n")

result = model_with_tools.invoke(messages)
print(type(result))
print(result)
print(f"\n最终回答: {result.content if result.content else '无内容'}")
