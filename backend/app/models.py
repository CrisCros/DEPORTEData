"""
Schemas Pydantic — request/response models.
"""

from pydantic import BaseModel, Field, ConfigDict


class LoginRequest(BaseModel):
    username: str
    password: str


class ChatRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    message: str = Field(min_length=1, alias="question")
