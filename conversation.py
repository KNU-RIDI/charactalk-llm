from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from character_loader import load_all_characters
from cachetools import TTLCache
from config import llm

sessions = TTLCache(maxsize=100, ttl=600)

chains = {}

def get_history(session_id):
    return sessions[session_id]

def get_prompt_text(char_data):
    return f"""
        너는 동화 속 {char_data['name']}처럼 말해야 해. {char_data['name']}의 경험과 감정을 녹여서 답변해야 해.
        답변을 할 때 동화 속 이야기를 참고해서, 동화 속 설정과 충돌나지 않도록 말해야 해.
        대답은 자연스럽게 대답해야 하며, 너무 긴 설명을 하지 않아야 해.
        현대적인 대화처럼 부드럽게 답변해야 해.
        대화할 때 형식적인 태그(AI: 등) 없이 자연스럽게 말해야 해.
        AI라고 자신을 지칭하지 말고, 캐릭터처럼 대화해야 해.
        """

def load_chains():
    characters = load_all_characters()
    for character in characters:
        prompt = ChatPromptTemplate.from_messages([
            ("system", get_prompt_text(character)),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        chains[character["id"]] = RunnableWithMessageHistory(
            prompt | llm,
            get_history,
            input_messages_key="input",
            history_messages_key="history"
        )
        
def get_chain(room_id, character_id):
    if room_id not in sessions:
        sessions[room_id] = ChatMessageHistory()
    return chains[int(character_id)]