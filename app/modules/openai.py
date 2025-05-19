import uuid
from fastapi import Request, HTTPException
from openai import OpenAI
from app.schemas.openai import ChatCompletionRequest
from logging import getLogger
from app.utils.config import OPENAI_API_KEY

api_logger = getLogger("devin_tokunou_api.api")

def get_request_id(request: Request) -> str:
    """Get request ID from state or generate a new one if not present"""
    try:
        return request.state.request_id
    except AttributeError:
        return str(uuid.uuid4())

def get_openai_client():
    """Initialize and return an OpenAI client with appropriate API key"""
    return OpenAI(api_key=OPENAI_API_KEY)

def create_chat_completion(request: Request, chat_request: ChatCompletionRequest):
    """Create a chat completion using OpenAI API"""
    request_id = get_request_id(request)
    api_logger.info(f"OpenAI chat completion request - Request ID: {request_id}")
    
    try:
        client = get_openai_client()
        
        api_logger.info(f"Model: {chat_request.model}, Messages count: {len(chat_request.messages)} - Request ID: {request_id}")
        
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
        
        api_logger.info(f"OpenAI chat completion successful - Request ID: {request_id}")
        return mock_response
        
    except Exception as e:
        api_logger.error(f"OpenAI chat completion failed - Error: {str(e)} - Request ID: {request_id}")
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

def list_available_models(request: Request):
    """List available OpenAI models"""
    request_id = get_request_id(request)
    api_logger.info(f"OpenAI list models request - Request ID: {request_id}")
    
    try:
        mock_models = {
            "data": [
                {"id": "gpt-3.5-turbo", "object": "model", "created": 1677610602},
                {"id": "gpt-4", "object": "model", "created": 1677649963},
                {"id": "text-embedding-ada-002", "object": "model", "created": 1671217299}
            ]
        }
        
        api_logger.info(f"OpenAI list models successful - Request ID: {request_id}")
        return mock_models
        
    except Exception as e:
        api_logger.error(f"OpenAI list models failed - Error: {str(e)} - Request ID: {request_id}")
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
