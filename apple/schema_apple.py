from typing import Optional
from pydantic import BaseModel

    
class AppleAuthRequest(BaseModel):
    id_token: str
    nonce: str
    user_identifier: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    
class AppleSignInResponse(BaseModel):
    access_token: str
    refresh_token: str
    access_token_expires_at: float
    refresh_token_expires_at: float
    user_id: str
    email: str | None
    is_verified: bool
    
class AccessTokenResponse(BaseModel):
    access_token: str
    access_token_expires_at: float
    
class RefreshTokenRequest(BaseModel):
    refresh_token: str
    
class RefreshTokenResponse(BaseModel):
    refresh_token: str
    refresh_token_expires_at: float