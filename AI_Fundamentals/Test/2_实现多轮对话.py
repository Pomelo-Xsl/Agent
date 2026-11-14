from langchain_community.chat_models import ChatTongyi

class MultiTurnChat:
    def __init__(self,model:str,system_prompt:str = None) -> None:
        self.llm = ChatTongyi(
            model = model,
            streaming=True
        )
        self.chat_history = []
        if system_prompt:
            self.chat_history.append(('system',system_prompt))

    def add_user_message(self,content:str) -> None:
        self.chat_history.append(("human",content))

    def add_ai_message(self,content:str) -> None:
        self.chat_history.append(("ai",content))

    def send(self, user_message:str):
        # 1.添加用户消息到历史
        self.add_user_message(user_message)
        # 2.直接使用history 调用模型进行流式输出
        stream = self.llm.stream(input=self.chat_history)
        # 3.收集完整并逐块返回
        full_reply=""
        for chunk in stream:
            if chunk.content:
                full_reply += chunk.content
                yield chunk.content
        # 4.添加模型的完整回复到历史
        self.add_ai_message(full_reply)


if __name__ == '__main__':
    #1.配置参数
    MODEL = "deepseek-v4-pro-0813"
    SYSTEM_MESSAGE = "背景设定：你现在是一个AI老师，负责AI课程"
    #2.创建多论对话对象
    chat = MultiTurnChat(
        model=MODEL,
        system_prompt=SYSTEM_MESSAGE
    )
    print("多论对话已启动，输入内容按回车发送，输入'exit'或'quit'退出程序")
    #循环接受客户输入并回答
    while True:
        #获取用户输入
        user_input = input("human:")
        #退出条件判断
        if user_input.strip() in ('exit','quit'):
            print("对话结束,拜拜")
            break
        if not user_input.strip():
            print("请勿输入空白字符")
            continue
        #调用模型并回复
        print("AI老师:",end='',flush=True)
        for chunk in chat.send(user_input):
            print(chunk,end='',flush=True)
        print()
