from fastapi import APIRouter, Request, Depends, HTTPException, Response
from fastapi.responses import RedirectResponse
from app.modules.auth.ms_graph import get_auth_url, get_token_from_code, get_user_info
from app.schemas.auth.ms_graph import TokenResponse, UserInfo
from app.utils.logger import api_logger
from typing import Optional

router = APIRouter(
    prefix="/auth/ms-graph",
    tags=["auth"],
    responses={
        401: {"description": "Authentication failed"},
        500: {"description": "Server error"}
    },
)

@router.get("/login")
async def login(request: Request):
    """
    Redirect to Microsoft login page for authentication
    """
    request_id = getattr(request.state, "request_id", None)
    api_logger.info(f"Microsoft Graph API login request - Request ID: {request_id or ''}")
    
    try:
        # Generate authorization URL and redirect user
        auth_url = get_auth_url(request_id)
        api_logger.info(f"Redirecting to Microsoft login - Request ID: {request_id or ''}")
        return RedirectResponse(url=auth_url)
    except Exception as e:
        api_logger.error(f"Failed to generate auth URL: {str(e)} - Request ID: {request_id or ''}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initiate authentication: {str(e)}"
        )

@router.get("/callback")
async def callback(request: Request, code: Optional[str] = None, state: Optional[str] = None, error: Optional[str] = None):
    """
    Handle callback from Microsoft authentication
    """
    request_id = getattr(request.state, "request_id", None) or state
    api_logger.info(f"Microsoft Graph API callback received - Request ID: {request_id or ''}")
    
    # Check for authentication errors
    if error:
        api_logger.error(f"Authentication error: {error} - Request ID: {request_id or ''}")
        return {"error": error, "message": "Authentication failed"}
    
    # Validate authorization code
    if not code:
        api_logger.error(f"No authorization code provided - Request ID: {request_id or ''}")
        raise HTTPException(
            status_code=400,
            detail="No authorization code provided"
        )
    
    try:
        # Exchange authorization code for access token
        token_response = get_token_from_code(code, request_id)
        
        # Get user information using the access token
        user_info = get_user_info(token_response.access_token, request_id)
        
        api_logger.info(f"Authentication successful for user: {user_info.display_name} - Request ID: {request_id or ''}")
        
        # Return authentication result
        return {
            "authenticated": True,
            "user": user_info,
            "token_info": {
                "token_type": token_response.token_type,
                "expires_in": token_response.expires_in,
                "scope": token_response.scope
            }
        }
    except Exception as e:
        api_logger.error(f"Authentication callback error: {str(e)} - Request ID: {request_id or ''}")
        raise HTTPException(
            status_code=500,
            detail=f"Authentication failed: {str(e)}"
        )

@router.get("/me")
async def get_me(request: Request, token: str):
    """
    Get user information using an access token
    """
    request_id = getattr(request.state, "request_id", None)
    api_logger.info(f"Request to get user info - Request ID: {request_id or ''}")
    
    try:
        user_info = get_user_info(token, request_id)
        return user_info
    except Exception as e:
        api_logger.error(f"Failed to get user info: {str(e)} - Request ID: {request_id or ''}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get user information: {str(e)}"
        )
