from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import Any
from .prompt import INTENT_RECOGNIZE_WITH_STRUCTURED_OUTPUT_PROMPT

class IntentResult(BaseModel):
    """意图识别结果：通过大语言模型识别用户输入的意图，输出结构化数据。"""
    intents: list[str] = Field(description="意图列表，每个元素为一个意图名称")
    slots: dict[str, Any] = Field(description="slot值字典，键为slot名称，值为slot值")
    confidence: float = Field(description="置信度分数，取值范围0~1，越大表示越确信该意图")


class IntentRecognizer:
    """
    意图识别器：通过大语言模型识别用户输入的意图，输出IntentResult对象
    """

    def __init__(self, llm: ChatTongyi):
        # chain = prompt | model | outputparser
        self.__prompt = ChatPromptTemplate.from_messages([
            ("system", INTENT_RECOGNIZE_WITH_STRUCTURED_OUTPUT_PROMPT),
            ("ai", "上下文内容：{chat_history}"),
            ("human", "用户输入：{user_input}")
        ])
        self.__llm = llm.with_structured_output(IntentResult)
        self.__chain = self.__prompt | self.__llm

    def recognize(self, user_input: str, chat_history: str | None = None) -> IntentResult:
        chat_history = chat_history if chat_history else ""
        result = self.__chain.invoke(input={"chat_history": chat_history, "user_input": user_input})
        # IntentResult result
        if result is None:
            print(f"{user_input} 的结构化输出为 None")
            result = IntentResult(
                intents=["general"],
                slots={},
                confidence=0.0
            )
        return result
