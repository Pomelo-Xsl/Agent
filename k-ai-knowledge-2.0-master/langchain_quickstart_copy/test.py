from langchain_community.chat_models import ChatTongyi

# class ChatTongyi(BaseChatModel): langchain_community 实现类的包
# class BaseChatModel(BaseLanguageModel[AIMessage], ABC):

from langchain_community.llms.tongyi import Tongyi
# class Tongyi(BaseLLM):
# class BaseLLM(BaseLanguageModel[str], ABC):

from langchain_community.embeddings import DashScopeEmbeddings
# class DashScopeEmbeddings(Embeddings):