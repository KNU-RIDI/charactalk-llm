import os

from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, FileResponse
from conversation import get_chain, load_chains

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

headers = {"Content-Type": "text/event-stream; charset=utf-8"}

@app.get("/")
async def serve_index():
    index_path = os.path.join("static", "index.html")
    return FileResponse(index_path)

def message_format(message):
    return f"data: {message}\n\n"

@app.get("/generate/{room_id}")
async def generate_message(
    room_id: str, 
    char_id: str = Query(..., alias="charId"),
    user_input: str = Query(..., alias="message")
):
    if not user_input: return StreamingResponse(message_format("메시지가 없습니다."), headers=headers)
    
    chain = get_chain(room_id, char_id)

    async def generate_response():
        for chunk in chain.stream(
            { "input": user_input },
            config={ "configurable": { "session_id": room_id }}
        ):
            yield message_format(chunk)
    
    return StreamingResponse(generate_response(), headers=headers)

if __name__ == "__main__":
    import uvicorn
    load_chains()
    uvicorn.run(app, host="0.0.0.0", port=8000)