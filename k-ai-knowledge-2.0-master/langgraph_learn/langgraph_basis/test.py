import operator

from langgraph.graph import StateGraph
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
graph.add_edge("__start__", "node_a")
graph.add_edge("node_a", "node_b")

# 创建检查点
saver = InMemorySaver()

# 编译图时启用检查点
graph = graph.compile(checkpointer=saver)

config = {"configurable": {"thread_id": "1"}}
graph.invoke({"foo": "", "bar": []}, config=config)

# 获取最新的状态快照
# snapshot = graph.get_state(config)
# print(snapshot)
# config = {
#   "configurable": {
#     "thread_id": "1",
#     "checkpoint_id": snapshot.parent_config.get('configurable')['checkpoint_id'],
#   },
# }
# print(graph.get_state(config))

# r = graph.get_state_history(config)
# print(list(r))
#
