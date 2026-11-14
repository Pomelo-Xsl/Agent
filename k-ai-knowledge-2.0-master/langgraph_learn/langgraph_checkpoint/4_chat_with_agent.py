from langchain_community.chat_models.tongyi import ChatTongyi
from langchain.tools import tool
from agent import create_agent
from langchain_core.messages import HumanMessage


# ==========================
# 定义工具
# ==========================
@tool
def get_weather(location: str) -> str:
    """查询天气信息"""
    return f"今天{location}的温度是 100℃"


@tool
def multiply(a: int, b: int) -> str:
    """将 a 和 b 相乘"""
    return str(a * b)

# ==========================
# 初始化模型和Agent
# ==========================

model = ChatTongyi(
    model="qwen3-max"
)

tools = [
    get_weather,
    multiply
]
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="你是一个智能助手，可以查询天气和进行数学计算。"
)


# ==========================
# 创建会话线程
# ==========================
config = {
    "configurable": {
        "thread_id": "user-001"
    }
}

# ==========================
# 多轮对话
# ==========================
print("智能助手已启动，输入 exit 退出")
while True:
    user_input = input("\n用户：")

    if user_input == "exit":
        print("对话结束")
        break

    result = agent.invoke(
        {
            "messages": [HumanMessage(content=user_input)]
        },
        config=config
    )
    print("助手：", result["messages"][-1].content)