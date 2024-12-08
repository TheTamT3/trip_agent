from pydantic import BaseModel


class Request(BaseModel):
    text: str
    sender_id: str


class Response(BaseModel):
    status: str = "success"
    answer: str


class Message(BaseModel):
    query: str
    answer: str
    sender_id: str = None
