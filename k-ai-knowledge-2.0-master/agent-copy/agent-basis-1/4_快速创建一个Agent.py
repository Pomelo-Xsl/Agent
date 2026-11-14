from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool


# 1.创建 tool
@tool
def get_goods_info_by_id(goods_id: int) -> str | None:
    """
    根据商品goods_id去查询商品信息
    :param goods_id: 商品id
    :return: 查询到的商品信息，没查询到就返回空
    """
    goods_info = {
        1: "爱疯手机",
        2: "华为电脑"
    }
    if goods_id not in goods_info:
        print(f"id为{goods_id}的商品不存在")
        return None
    goods = goods_info[goods_id]
    print(f"id为{goods_id}的商品为：{goods}")
    return goods


# 2.创建 Agent
tools = [get_goods_info_by_id]
agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),
    tools=tools,
    system_prompt="你是一个商品信息查询助手，如果用户传入商品ID，请你帮他查询是什么商品"
)

# 3.调用 agent 去帮我们查询商品信息
user_query = "商品ID为1，这是一个什么商品？"
result = agent.invoke(
    {"messages": [{"role": "user", "content": user_query}]}
)

# 4.打印结果
print(type(result)) # <class 'dict'>
# print(result)
# print(result['messages'])
print(result['messages'][-1].content)

"""
result['messages']:
[HumanMessage(content='商品ID为1，这是一个什么商品？', additional_kwargs={}, response_metadata={}, id='4e1e3f63-1b1f-4e11-a08d-b0fbff80d301'), 

AIMessage(content='', additional_kwargs={'tool_calls': [{'function': {'arguments': '{"goods_id": 1}', 'name': 'get_goods_info_by_id'}, 
'id': 'call_f471ee4781c848b1866ac035', 'index': 0, 'type': 'function'}]}, 
response_metadata={'model_name': 'qwen3-max', 'finish_reason': 'tool_calls', 'request_id': '6cbcd0c0-66d2-99d0-88ae-90791baf9aaf', 'token_usage': {'input_tokens': 310, 'output_tokens': 25, 'prompt_tokens_details': {'cached_tokens': 0}, 'total_tokens': 335}}, id='lc_run--019f0d28-ce45-7902-995a-041bdde32a59-0', 
tool_calls=[{'name': 'get_goods_info_by_id', 'args': {'goods_id': 1}, 'id': 'call_f471ee4781c848b1866ac035', 'type': 'tool_call'}], invalid_tool_calls=[]), 

ToolMessage(content='爱疯手机', name='get_goods_info_by_id', id='197e6381-2530-4b88-8165-ad7377fccdf0', tool_call_id='call_f471ee4781c848b1866ac035'), 

AIMessage(content='商品ID为1的商品是“爱疯手机”。', additional_kwargs={}, response_metadata={'model_name': 'qwen3-max', 'finish_reason': 'stop', 'request_id': '02ee4cfb-b9d7-9090-a3c2-fcce6bf28bc0', 'token_usage': {'input_tokens': 353, 'output_tokens': 11, 'prompt_tokens_details': {'cached_tokens': 192}, 'total_tokens': 364}}, id='lc_run--019f0d28-d361-71f2-8ff2-4f2f301ae49b-0', tool_calls=[], invalid_tool_calls=[])]

"""



























