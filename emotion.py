from config import llm
from enum import Enum

class Emotion(Enum):
  NEUTRAL = "NEUTRAL"
  HAPPY = "HAPPY"
  EXCITED = "EXCITED"
  SAD = "SAD"
  SHY = "SHY"
  SURPRISED = "SURPRISED"
  ANNOYED = "ANNOYED"

def get_prompt_text(message):
  return f"""
      너는 메시지의 감정을 분석해고, 단 하나의 감정으로 대답해야 해. 아에 다른 말은 하지 말고, 감정만 대답해야 해.

      감정에는 다음과 같은 것들이 있어.
      - NEUTRAL
      - HAPPY
      - EXCITED
      - SAD
      - SHY
      - SURPRISED
      - ANNOYED

      다음은 감정 분석을 위한 메시지야.
      {message}
      """

def analyze_emotion(message):
  prompt = get_prompt_text(message)
  response = llm(prompt)
  emotion = response.strip().upper()
  if emotion not in Emotion.__members__:
    raise ValueError(f"Invalid emotion: {emotion}")
  return Emotion[emotion]