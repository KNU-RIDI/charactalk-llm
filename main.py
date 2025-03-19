import asyncio
import os
import uuid

from fastapi import FastAPI, Request,  Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, FileResponse
from conversation import get_chain, load_chains
from cachetools import TTLCache

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

responses = TTLCache(maxsize=100, ttl=600)

headers = {"Content-Type": "text/event-stream; charset=utf-8"}

@app.get("/")
async def serve_index():
    index_path = os.path.join("static", "index.html")
    return FileResponse(index_path)

@app.post("/send/{room_id}")
async def send_message(room_id: str, request: Request, char_id: str = Query(..., alias="charId")):
    data = await request.json()
    user_input = data.get("message", "")

    if not user_input: return {"error": "메시지를 입력해주세요."}
    
    chain = get_chain(room_id, char_id)
    
    response_id = str(uuid.uuid4())
    responses[response_id] = asyncio.Queue()

    async def generate_response():
        for chunk in chain.stream(
            { "input": user_input },
            config={ "configurable": { "session_id": room_id }}
        ):
            await responses[response_id].put(chunk)
        await responses[response_id].put(None)

    asyncio.create_task(generate_response()) 
    
    return { "data": response_id }

@app.get("/stream/{response_id}")
async def stream_chat(response_id: str):
    if response_id not in responses:
        return StreamingResponse(iter(["존재하지 않는 응답입니다."]), headers=headers)

    response_queue = responses[response_id]

    async def event_generator():
        while True:
            chunk = await response_queue.get()
            if chunk is None: break 
            yield f"data: {chunk}\n\n"  
        responses.pop(response_id)
        
    return StreamingResponse(event_generator(), headers=headers)

if __name__ == "__main__":
    import uvicorn
    load_chains()
    uvicorn.run(app, host="0.0.0.0", port=8000)