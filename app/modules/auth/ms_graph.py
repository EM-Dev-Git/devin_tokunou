import os
import msal
import requests
from fastapi import HTTPException, Request
from app.schemas.auth.ms_graph import AuthConfig, TokenResponse, UserInfo
from app.utils.logger import api_logger

# Default scopes for Microsoft Graph API
DEFAULT_SCOPES = ["User.Read", "Mail.Read"]

def get_auth_config() -> AuthConfig:
    """Get authentication configuration from environment variables"""
    tenant_id = os.environ.get("MS_GRAPH_TENANT_ID")
    client_id = os.environ.get("MS_GRAPH_CLIENT_ID")
    client_secret = os.environ.get("MS_GRAPH_CLIENT_SECRET")
    redirect_uri = os.environ.get("MS_GRAPH_REDIRECT_URI")
    
    if not all([tenant_id, client_id, client_secret, redirect_uri]):
        api_logger.error("Missing required Microsoft Graph API configuration")
        raise HTTPException(
            status_code=500,
            detail="Microsoft Graph API configuration is incomplete. Please check environment variables."
        )
    
    # Get scopes from environment or use defaults
    scopes_str = os.environ.get("MS_GRAPH_SCOPES", " ".join(DEFAULT_SCOPES))
    scopes = scopes_str.split()
    
    # Build authority URL
    authority = os.environ.get(
        "MS_GRAPH_AUTHORITY", 
        f"https://login.microsoftonline.com/{tenant_id}"
    )
    
    return AuthConfig(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scopes=scopes,
        authority=authority
    )

def get_msal_app():
    """Get MSAL confidential client application"""
    config = get_auth_config()
    
    return msal.ConfidentialClientApplication(
        client_id=config.client_id,
        client_credential=config.client_secret,
        authority=config.authority
    )

def get_auth_url(request_id: str = None) -> str:
    """Get authorization URL for Microsoft Graph API"""
    config = get_auth_config()
    app = get_msal_app()
    
    # Generate authorization URL
    auth_url = app.get_authorization_request_url(
        scopes=config.scopes,
        redirect_uri=config.redirect_uri,
        state=request_id or "",
        prompt="select_account"
    )
    
    if request_id:
        api_logger.info(f"Generated auth URL - Request ID: {request_id}")
    
    return auth_url

def get_token_from_code(code: str, request_id: str = None) -> TokenResponse:
    """Get access token from authorization code"""
    config = get_auth_config()
    app = get_msal_app()
    
    # Acquire token by authorization code
    result = app.acquire_token_by_authorization_code(
        code=code,
        scopes=config.scopes,
        redirect_uri=config.redirect_uri
    )
    
    if "error" in result:
        api_logger.error(f"Error acquiring token: {result.get('error_description')} - Request ID: {request_id or ''}")
        raise HTTPException(
            status_code=401,
            detail=f"Authentication failed: {result.get('error_description')}"
        )
    
    if request_id:
        api_logger.info(f"Token acquired successfully - Request ID: {request_id}")
    
    return TokenResponse(
        access_token=result.get("access_token"),
        token_type=result.get("token_type"),
        expires_in=result.get("expires_in"),
        scope=result.get("scope"),
        refresh_token=result.get("refresh_token"),
        id_token=result.get("id_token")
    )

def get_user_info(token: str, request_id: str = None) -> UserInfo:
    """Get user information from Microsoft Graph API"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Call Microsoft Graph API to get user information
    response = requests.get(
        "https://graph.microsoft.com/v1.0/me",
        headers=headers
    )
    
    if response.status_code != 200:
        api_logger.error(f"Error getting user info: {response.text} - Request ID: {request_id or ''}")
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Failed to get user information: {response.text}"
        )
    
    user_data = response.json()
    
    if request_id:
        api_logger.info(f"User info retrieved successfully - Request ID: {request_id}")
    
    return UserInfo(
        id=user_data.get("id"),
        display_name=user_data.get("displayName"),
        email=user_data.get("mail"),
        user_principal_name=user_data.get("userPrincipalName"),
        additional_info=user_data
    )
