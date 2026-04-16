# Schemas Pydantic — request/response models.

from pydantic import BaseModel, Field, ConfigDict


class LoginRequest(BaseModel):
    username: str
    password: str


class ChatRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    message: str = Field(min_length=1, alias="question")


class AddUserRequest(BaseModel):
    """Payload para /internal/db/add_user."""
    username: str = Field(min_length=1, max_length=100)
    pwd: str = Field(min_length=4, max_length=200)
    role: str = Field(default="user", max_length=50)
