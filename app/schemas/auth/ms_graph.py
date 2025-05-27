from pydantic import BaseModel
from typing import Dict, List, Optional, Any

class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token: str
    token_type: str
    expires_in: int
    scope: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None

class AuthConfig(BaseModel):
    """Schema for authentication configuration"""
    tenant_id: str
    client_id: str
    client_secret: str
    redirect_uri: str
    scopes: List[str]
    authority: Optional[str] = None

class UserInfo(BaseModel):
    """Schema for user information from Microsoft Graph API"""
    id: str
    display_name: str
    email: Optional[str] = None
    user_principal_name: str
    additional_info: Optional[Dict[str, Any]] = None
