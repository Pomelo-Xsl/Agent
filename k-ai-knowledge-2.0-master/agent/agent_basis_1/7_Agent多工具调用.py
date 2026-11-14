from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool
from langchain.agents import create_agent

# 2. 工具调用
# 2.1. 模拟商品数据库
product_db = {
    "iPhone": {"id": 101, "price": 5999},
    "MacBook": {"id": 102, "price": 12999},
    "小米手机": {"id": 103, "price": 3999},
}

# 2.2. 工具A：根据名称获取ID
@tool(description="根据商品名称获取对应的商品ID")
def get_product_id_by_name(name: str) -> int | None:
    """输入商品名称（如'iPhone'），返回商品ID"""
    name_lower = name.lower()
    for prod_name, info in product_db.items():
        if prod_name.lower() == name_lower:
            print(f"[工具A] 商品 '{name}' 的 ID 是 {info['id']}")
            return info['id']
    print(f"[工具A] 未找到商品 '{name}'")
    return None

# 2.3. 工具B：根据ID获取价格
@tool(description="根据商品ID查询商品价格")
def get_product_price_by_id(product_id: int) -> str | None:
    """输入商品ID，返回价格字符串"""
    for prod_name, info in product_db.items():
        if info['id'] == product_id:
            price = info['price']
            print(f"[工具B] ID {product_id} 的商品 '{prod_name}' 价格为 {price} 元")
            return f"{prod_name} 的价格是 {price} 元"
    print(f"[工具B] 未找到 ID {product_id} 对应的商品")
    return None

# 3. 创建 Agent
agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),
    tools=[get_product_id_by_name, get_product_price_by_id],
    system_prompt="你是一个商品查询助手。当用户询问某个商品的价格时，请先调用 get_product_id_by_name 获取商品ID，"
           "然后再调用 get_product_price_by_id 获取价格，最后把价格告知用户。"
)

# 4. 调用 Agent 执行任务
user_query = "我想知道小米手机的价格是多少？"
print(f"用户问题：{user_query}\n")

# 调用 agent 并打印结果
result = agent.invoke({
    "messages": [{"role": "user", "content": user_query}]
})

# 5. 提取最终回答
final_answer = result["messages"][-1].content
print(f"\n最终回答：{result}\n")
print(f"\n最终回答：{result['messages']}\n")
print(f"\n最终回答：{len(result['messages'])}")