from fastapi import APIRouter, Request
from app.modules.openai import create_chat_completion, list_available_models
from app.schemas.openai import ChatCompletionRequest, ChatCompletionResponse

router = APIRouter(
    prefix="/openai",
    tags=["openai"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "OpenAI API error"}
    },
)

@router.post("/chat/completions", response_model=ChatCompletionResponse)
async def create_chat_completion_endpoint(request: Request, chat_request: ChatCompletionRequest):
    """
    Create a chat completion using OpenAI API
    """
    return create_chat_completion(request, chat_request)

@router.get("/models")
async def list_models_endpoint(request: Request):
    """
    List available OpenAI models
    """
    return list_available_models(request)
