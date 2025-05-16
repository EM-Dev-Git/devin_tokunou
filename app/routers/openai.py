from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from openai import OpenAI
from app.utils.logger import api_logger

DUMMY_OPENAI_API_KEY = "sk-dummy-api-key-for-development-purposes-only"

router = APIRouter(
    prefix="/openai",
    tags=["openai"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "OpenAI API error"}
    },
)

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str = "gpt-3.5-turbo"
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 150

class ChatCompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Dict[str, Any]]
    usage: Dict[str, int]

def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY", DUMMY_OPENAI_API_KEY)
    return OpenAI(api_key=api_key)

@router.post("/chat/completions", response_model=ChatCompletionResponse)
async def create_chat_completion(request: Request, chat_request: ChatCompletionRequest):
    """
    Create a chat completion using OpenAI API
    """
    api_logger.info(f"OpenAI chat completion request - Request ID: {request.state.request_id}")
    
    try:
        client = get_openai_client()
        
        api_logger.info(f"Model: {chat_request.model}, Messages count: {len(chat_request.messages)} - Request ID: {request.state.request_id}")
        
        
        mock_response = {
            "id": "chatcmpl-dummy-id",
            "object": "chat.completion",
            "created": 1683123456,
            "model": chat_request.model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "This is a dummy response from the OpenAI API. In a real implementation, this would be the actual response from the OpenAI API."
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 20,
                "total_tokens": 30
            }
        }
        
        api_logger.info(f"OpenAI chat completion successful - Request ID: {request.state.request_id}")
        return mock_response
        
    except Exception as e:
        api_logger.error(f"OpenAI chat completion failed - Error: {str(e)} - Request ID: {request.state.request_id}")
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

@router.get("/models")
async def list_models(request: Request):
    """
    List available OpenAI models
    """
    api_logger.info(f"OpenAI list models request - Request ID: {request.state.request_id}")
    
    try:
        
        mock_models = {
            "data": [
                {"id": "gpt-3.5-turbo", "object": "model", "created": 1677610602},
                {"id": "gpt-4", "object": "model", "created": 1677649963},
                {"id": "text-embedding-ada-002", "object": "model", "created": 1671217299}
            ]
        }
        
        api_logger.info(f"OpenAI list models successful - Request ID: {request.state.request_id}")
        return mock_models
        
    except Exception as e:
        api_logger.error(f"OpenAI list models failed - Error: {str(e)} - Request ID: {request.state.request_id}")
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
