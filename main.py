import asyncio
from character_loader import load_character
from conversation import create_conversation_chain

async def typewriter_effect(text, delay=0.05):
    for char in text:
        print(char, end="", flush=True)
        await asyncio.sleep(delay)
    print()

async def main():
    while True:
        character_name = input("🎭 대화할 캐릭터를 입력하세요: ")
        char_data = load_character(character_name)
        if char_data: break
        print("❌ 해당 캐릭터 데이터를 찾을 수 없습니다. 다시 입력해주세요.")

    session_id = "user_1234"  # 고유한 세션 ID
    conversation_chain = create_conversation_chain(char_data)

    print(f"✨ {char_data['name']}와 대화를 시작합니다. 'exit' 또는 '종료'를 입력하면 종료됩니다. ✨")

    while True:
        user_input = input("👤: ")
        if user_input.lower() in ["exit", "종료"]:
            print(f"{char_data['name']}: 소중한 대화였어요! 언젠가 다시 만나요.")
            break

        response = conversation_chain.invoke(
            {"input": user_input },
            config={"configurable": {"session_id": session_id}}
        )

        print(f"{char_data['name']}: ", end="")
        await typewriter_effect(response)

asyncio.run(main())
