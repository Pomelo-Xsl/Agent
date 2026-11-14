from typing import TypedDict
from typing_extensions import NotRequired

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command


# ============================================================
# 1. 定义 State
# ============================================================
class State(TypedDict):
    amount: int
    # 人工确认！
    approved: bool

# ============================================================
# 2. 定义节点
# ============================================================

def apply_refund(state: State):
    """准备退款"""
    print(f"准备退款：{state['amount']} 元")
    return {}

def human_review(state: State):
    print(f"before：人工审批 {state}")
    # 人工介入
    # approved = True
    approved = interrupt({
        "message": "退款金额较大，请人工审批",
        "amount": state["amount"]
    })
    print(f"after：人工审批 {approved} {state}")

    return {
        "approved": approved
    }

def execute_refund(state: State):
    """真正执行退款"""
    if state["approved"]:
        print("审批通过，执行退款")
        print(f"成功退款：{state['amount']} 元")
    else:
        print("审批拒绝，不执行退款")
    return {}

# ============================================================
# 3. 创建 Graph
# ============================================================
builder = StateGraph(State)

builder.add_node("apply_refund", apply_refund)
builder.add_node("human_review", human_review)
builder.add_node("execute_refund", execute_refund)

builder.add_edge(START, "apply_refund")
builder.add_edge("apply_refund", "human_review")
builder.add_edge("human_review", "execute_refund")
builder.add_edge("execute_refund", END)


# ============================================================
# 4. 配置 Checkpointer
# ============================================================
from json_file_saver import JsonFileSaver
checkpointer = JsonFileSaver("checkpoint.json")

graph = builder.compile(
    checkpointer=checkpointer
)

# ============================================================
# 5. 配置 thread_id
# ============================================================
config = {
    "configurable": {
        "thread_id": "refund-001"
    }
}

# ============================================================
# 6. 第一次执行
# ============================================================

# result = graph.invoke(
#     {
#         "amount": 5000
#     },
#     config=config
# )
# print(result)
for idx, snapshot in enumerate(graph.get_state_history(config)):
    print(idx, snapshot)

# ============================================================
# 7. 判断是否进入人工审批
# ============================================================
# print("\n请选择：")
# print("1. 同意退款")
# print("2. 拒绝退款")
# # ========================================================
# # 8. 等待人工输入
# # ========================================================
# while True:
#     choice = input("\n请输入 1 或 2：").strip()
#     if choice == "1":
#         approved = True
#         print("\n人工操作：同意退款")
#         break
#     elif choice == "2":
#         approved = False
#         print("\n人工操作：拒绝退款")
#         break
#     else:
#         print("输入错误，请输入 1 或 2")
#
# # ========================================================
# # 9. 恢复 Graph
# # ========================================================
# result = graph.invoke(
#     Command(resume=approved),
#     config=config
# )
#
#
#
#
#
#

















































