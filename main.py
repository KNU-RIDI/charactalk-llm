import os
import json
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from conversation import get_chain, load_chains
from datetime import datetime
from more_itertools import peekable
from tts import synthesize_streaming

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

headers = {"Content-Type": "text/event-stream; charset=utf-8"}

def get_local_timestamp():
    return datetime.now().replace(microsecond=0).isoformat()

def format_chat_stream_response(name: str, token: str, is_final: bool) -> str:
    payload = {
        "name": name,
        "token": token,
        "isFinal": is_final,
        "timestamp": get_local_timestamp()
    }
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"

@app.get("/generate/{room_id}")
def generate_message(
    room_id: str,
    char_id: str = Query(..., alias="charId"),
    user_input: str = Query(..., alias="message")
):
    print(f"🎯 FastAPI received: {user_input}, char_id: {char_id}, room_id: {room_id}")
    
    if not user_input:
        return StreamingResponse(
            iter([format_chat_stream_response("SYSTEM", "메시지가 없습니다.", True)]),
            headers=headers
        )

    chain = get_chain(room_id, char_id)

    def generate():
        print("🌱 stream 시작")
        try:
            chunks = peekable(chain.stream(
                {"input": user_input},
                config={"configurable": {"session_id": room_id}}
            ))

            for chunk in chunks:
                token = getattr(chunk, "content", str(chunk)).strip()
                is_final = not chunks.peek(None)  # 다음이 없으면 마지막
                print(f"🌿 [CHUNK] {token} (isFinal={is_final})")
                yield format_chat_stream_response(char_id, token, is_final)

        except Exception as e:
            print("🔥 에러 발생:", e)
            yield format_chat_stream_response("SYSTEM", "Error", True)

    return StreamingResponse(generate(), headers=headers)

@app.get("/speech/{room_id}")
def speech(
    room_id: str,
    char_id: str = Query(..., alias="charId"),
    user_input: str = Query(..., alias="message")
):
    print(f"🎯 received: {user_input}, char_id: {char_id}, room_id: {room_id}")
    
    chain = get_chain(room_id, char_id)

    def generate():
        chunks = chain.stream(
            { "input": user_input },
            config={ "configurable": { "session_id": room_id }}
        )
        yield from synthesize_streaming(chunks)

    return StreamingResponse(generate(), media_type="audio/L16")

if __name__ == "__main__":
    import uvicorn
    load_chains()
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
