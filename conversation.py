from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnableLambda
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from config import llm

session_store = {}

def get_session_history(session_id):
    if session_id not in session_store:
        session_store[session_id] = ChatMessageHistory()
    return session_store[session_id]

def get_prompt_text(char_data):
    return f"""
        너는 동화 속 {char_data['name']}처럼 말해야 해. {char_data['name']}의 경험과 감정을 녹여서 답변해야 해.
        답변을 할 때 동화 속 이야기를 참고해서, 동화 속 설정과 충돌나지 않도록 말해야 해.
        대답은 짧고 자연스럽게 대답해야 하며, 너무 긴 설명을 하지 않아야 해.",
        현대적인 대화처럼 부드럽게 답변해야 해.
        답변을 할 땐 대화 내용만 반환해줘.
        """

def create_conversation_chain(char_data):
    prompt = ChatPromptTemplate.from_messages([
        ("system", get_prompt_text(char_data)),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])

    # ✅ 대화 체인 생성
    return RunnableWithMessageHistory(
        prompt | llm,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history"
    )