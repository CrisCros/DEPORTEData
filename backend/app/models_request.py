from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class ChatRequest(BaseModel):
    question: str