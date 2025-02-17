from debug import Debuggable
from langchain_community.chat_message_histories.file import FileChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai.chat_models import ChatOpenAI
import os

class Nena(Debuggable):
    def __init__(self, debug: bool = False):
        super().__init__(debug)
        self.model = os.getenv("OPENAI_MODEL_NAME")
        self.llm = ChatOpenAI(model_name=self.model)
        self.chat_histories_folder = os.getenv("CHAT_HISTORIES_FOLDER")
        self.sessions = {}

    def get_session(self, session_id: str) -> BaseChatMessageHistory:
        """Retrieve a chat history"""
        if session_id not in self.sessions:
            session_file = f"{self.chat_histories_folder}/{session_id}.json"
            self.sessions[session_id] = FileChatMessageHistory(file_path=session_file, encoding='utf8')
        return self.sessions[session_id]

    def ask_me(self, user_id: str, user_message: str) -> str:
        """Send a message to LLM and respond"""
        messages = []

        session = self.get_session(user_id)
        session_messages = session.messages

        if len(session_messages) < 1:
            messages.append(SystemMessage(content="You are an assistant named Nena. Please answer any questions with the most accurate and complete information possible. Be friendly and try to help the user as much as possible."))

        messages.append(HumanMessage(content=user_message))

        config = { "configurable": { "session_id": user_id } }

        with_message_history = RunnableWithMessageHistory(self.llm, self.get_session)
        response = with_message_history.invoke(messages, config=config)

        return response.content
