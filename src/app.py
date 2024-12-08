import uvicorn
from fastapi import FastAPI

from ._schemas import Request, Response
from .main import Application
from .store import MongoTrackerStore

app = FastAPI()
tracker_store = MongoTrackerStore()
chat_app = Application(tracker_store=tracker_store)


@app.post("/chat", response_model=Response)
async def chat(data: Request) -> Response:
    return Response(answer=await chat_app.chat(sender_id=data.sender_id, text=data.text))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
