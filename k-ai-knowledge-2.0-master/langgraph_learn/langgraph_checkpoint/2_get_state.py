from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from typing import TypedDict

class State(TypedDict):
    foo: str
    bar: list[str]

def node_a(state: State) -> State:
    return {"foo": "a", "bar": ["a"]}

def node_b(state: State) -> State:
    return {"foo": "b", "bar": ["b"]}

# 创建图
graph = StateGraph(State)
graph.add_node("node_a", node_a)
graph.add_node("node_b", node_b)

# 设置边
graph.add_edge(START, "node_a")
graph.add_edge("node_a", "node_b")
graph.add_edge("node_b", END)

# 创建检查点
saver = InMemorySaver()

# 编译图时启用检查点
graph = graph.compile(checkpointer=saver)

# 获取最新的状态快照
config = {"configurable": {"thread_id": "1"}}
result = graph.invoke({"foo": "", "bar": []}, config=config)
print(result['foo'], result['bar'])

# state = graph.get_state(config)
# print(state)

# 获取特定检查点 ID 的状态快照
# config = {"configurable": {"thread_id": "1", "checkpoint_id":state.parent_config['configurable']['checkpoint_id']}}
# state = graph.get_state(config)
# print(state)


# 获取状态历史
state_history = graph.get_state_history(config)
for snapshot in state_history:
    print(snapshot)
