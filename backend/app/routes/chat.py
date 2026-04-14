from fastapi import APIRouter, Depends, HTTPException

from app.models_request import ChatRequest
from app.services.data_service import DataService, get_data_service

router = APIRouter(tags=["chat"])


@router.post("/chat")
def chat(request: ChatRequest, data_service: DataService = Depends(get_data_service)):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="El campo 'message' no puede estar vacío")

    return {
        "message": request.message,
        "answer": data_service.answer_chat(request.message),
    }
