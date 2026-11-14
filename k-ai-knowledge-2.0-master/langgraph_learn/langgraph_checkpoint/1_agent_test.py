from langchain_community.chat_models.tongyi import ChatTongyi
from langchain.tools import tool
from agent import create_agent
from langchain_core.messages import HumanMessage


@tool
def get_weather(location: str) -> str:
    """查询天气信息"""
    return f"今天{location}的温度是 100℃"


@tool
def multiply(a: int, b: int) -> str:
    """将 a 和 b 相乘"""
    return str(a * b)


model = ChatTongyi(model="qwen3-max")
tools = [get_weather, multiply]

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="你是一个智能助手，可以查询天气和进行数学计算。"
)

config = {
    "configurable": {
        "thread_id": "conversation-001"
    }
}

result1 = agent.invoke(
    {
        "messages": [
            HumanMessage(content="你好，我叫阿苑。")
        ]
    },
    config=config
)
print("助手:", result1['messages'][-1].content)
state_snapshot = agent.get_state(config)
# print("状态值：", state_snapshot.values)
# # 查看消息
# for message in state_snapshot.values["messages"]:
#     print(
#         type(message).__name__,
#         message.content
#     )
print("状态值：", state_snapshot.values)
print("下一个节点：", state_snapshot.next)
print("Checkpoint 配置：", state_snapshot.config)
print("元数据：", state_snapshot.metadata)
print("创建时间：", state_snapshot.created_at)
print("上一个 Checkpoint：", state_snapshot.parent_config)
print("任务：", state_snapshot.tasks)


print()
history = agent.get_state_history(config)

for snapshot in history:
    print("=" * 50)
    print("Checkpoint ID：", snapshot.config)
    print("当前状态：", snapshot.values)
    print("下一个节点：", snapshot.next)

# config = {
#     "configurable": {
#         "thread_id": "conversation-001"
#     }
# }
#
# result2 = agent.invoke(
#     {
#         "messages": [
#             HumanMessage(content="我叫什么名字？")
#         ]
#     },
#     config=config
# )
# print("助手:", result2["messages"][-1].content)
# state_snapshot = agent.get_state(config)
#
# print(state_snapshot.values)