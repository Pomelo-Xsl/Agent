from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool
from langchain.agents import create_agent


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


# 2. 创建 Agent
agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),  # 给 Agent 提供大脑
    tools=[get_goods_info_by_id],  # 给 Agent 提供工具
    system_prompt="你是一个商品信息查询助手，如果用户传入商品ID，请你帮他查询是什么商品"
)

# 3.调用 agent 去帮我们查询商品信息
result = agent.invoke({
    "messages": [{"role": "user", "content": "商品id为1，这个是一个什么商品"}]
})

# 4.打印结果
print(type(result))  # <class 'dict'>
print(result)
print(result['messages'])
"""
[
  {
    "type": "human",
    "content": "商品id为1，这个是一个什么商品"
  },
  
  
  {
    "type": "ai",
    "content": "",
    "additional_kwargs": {
      "tool_calls": [
        {
          "function": {
            "arguments": "{\"goods_id\": 1}",
            "name": "get_goods_info_by_id"
          },
          "id": "call_5920205eaf72447fbb07491e",
          "index": 0,
          "type": "function"
        }
      ]
    },
    "response_metadata": {
      "model_name": "qwen3-max",
      "finish_reason": "tool_calls",
      "request_id": "1bb955c1-afae-9bc2-956d-7508c3c4e301",
      "token_usage": {
        "input_tokens": 310,
        "output_tokens": 25,
        "prompt_tokens_details": {
          "cached_tokens": 0
        },
        "total_tokens": 335
      }
    },
    "id": "lc_run--019f0c8b-0c09-7131-9325-0b331fe677bd-0",
    "tool_calls": [
      {
        "name": "get_goods_info_by_id",
        "args": {
          "goods_id": 1
        },
        "id": "call_5920205eaf72447fbb07491e",
        "type": "tool_call"
      }
    ],
    "invalid_tool_calls": []
  },
  
  
  {
    "type": "tool",
    "content": "爱疯手机",
    "name": "get_goods_info_by_id",
    "id": "33e05796-e750-4591-aaae-99129e20549e",
    "tool_call_id": "call_5920205eaf72447fbb07491e"
  },
  
  
  {
    "type": "ai",
    "content": "商品ID为1的商品是“爱疯手机”。",
    "additional_kwargs": {},
    "response_metadata": {
      "model_name": "qwen3-max",
      "finish_reason": "stop",
      "request_id": "a9620eef-6454-99de-a438-62ef253384b6",
      "token_usage": {
        "input_tokens": 353,
        "output_tokens": 11,
        "prompt_tokens_details": {
          "cached_tokens": 192
        },
        "total_tokens": 364
      }
    },
    "id": "lc_run--019f0c8b-13b3-7a50-923e-19984e8c7c9f-0",
    "tool_calls": [],
    "invalid_tool_calls": []
  }
  
]
"""
print(len(result['messages']))

print('\n' + '=' * 20)
for msg in result['messages']:
    print(f"消息类型：{type(msg).__name__}，消息内容：{msg}")
