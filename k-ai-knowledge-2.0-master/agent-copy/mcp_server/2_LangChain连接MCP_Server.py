import asyncio

from langchain_community.chat_models import ChatTongyi
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

async def main():
    # 1. 创建客户端
    client = MultiServerMCPClient(
        {
            "weather": {
                "transport": "stdio",
                "command": "python",
                "args": ["E:\\python\\k-ai-knowledge-2.0\\agent-copy\\mcp_server\\weather.py"],
            }
        }
    )

    # 2. 获取工具（使用 await）
    tools = await client.get_tools()

    # 3. 创建 agent
    agent = create_agent(
        model=ChatTongyi(model="qwen3-max"),
        tools=tools,
        system_prompt="你是一个助手，可以调用工具帮助用户解决问题"
    )

    # 4.使用 agent
    weather_response = await agent.ainvoke({"messages": [("user", "北京天气怎么样？")]})
    print(weather_response['messages'][-1].content)
    """
    {'messages': [HumanMessage(content='北京天气怎么样？', additional_kwargs={}, response_metadata={}, id='32c97bb2-a17c-462b-b73f-bb9899495cd2'), 
    AIMessage(content='', additional_kwargs={'tool_calls': [{'function': {'arguments': '{"city": "北京"}', 'name': 'get_current_weather'}, 'id': 'call_c816ef40ac0645d198493416', 'index': 0, 'type': 'function'}]}, response_metadata={'model_name': 'qwen3-max', 'finish_reason': 'tool_calls', 'request_id': '1f94c8b3-b10b-9cf1-80c3-fa647c3b10dd', 'token_usage': {'input_tokens': 429, 'output_tokens': 22, 'prompt_tokens_details': {'cached_tokens': 0}, 'total_tokens': 451}}, id='lc_run--019f5004-4e10-7b62-9f20-35db5ce8b58e-0', tool_calls=[{'name': 'get_current_weather', 'args': {'city': '北京'}, 'id': 'call_c816ef40ac0645d198493416', 'type': 'tool_call'}], invalid_tool_calls=[]),
     ToolMessage(content=[{'type': 'text', 'text': '北京当前天气：100°C，风速 0km/h，天气状况：☀️ 超级热', 'id': 'lc_82acb744-9e02-41a3-8065-62fbf25d7f50'}], name='get_current_weather', id='76f29dbf-c8ca-49ad-a1f2-4a832ff9cd7a', tool_call_id='call_c816ef40ac0645d198493416', artifact={'structured_content': {'result': '北京当前天气：100°C，风速 0km/h，天气状况：☀️ 超级热'}}), 
     AIMessage(content='北京当前的天气是100°C，风速为0km/h，天气状况为晴天（☀️），非常炎热！请注意防暑降温，避免长时间暴露在户外，多补充水分以防中暑。', additional_kwargs={}, response_metadata={'model_name': 'qwen3-max', 'finish_reason': 'stop', 'request_id': 'c3f8f275-44ab-9148-aa80-9abf277bc8fc', 'token_usage': {'input_tokens': 492, 'output_tokens': 47, 'prompt_tokens_details': {'cached_tokens': 320}, 'total_tokens': 539}}, id='lc_run--019f5004-586b-7920-b908-006bab35aa10-0', tool_calls=[], invalid_tool_calls=[])]}
    """


if __name__ == '__main__':
    asyncio.run(main())
