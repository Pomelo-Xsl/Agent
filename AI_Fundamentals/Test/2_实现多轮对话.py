from langchain_community.chat_models import ChatTongyi

class MultiTurnChat:
    def __init__(self,model:str,system_prompt:str = None) -> None:
