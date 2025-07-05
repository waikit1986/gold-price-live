from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends

from . functions_apple import verify_apple_token
from . schema_apple import AppleAuthRequest, AppleSignInResponse, AccessTokenResponse, RefreshTokenRequest, RefreshTokenResponse
from db.database import get_db
from user.models_user import User
from auth.tokens import create_access_token, create_refresh_token, decrypt_token


router = APIRouter(
    prefix="/apple",
    tags=["Apple Authentication"]
)


@router.post("/login", response_model=AppleSignInResponse)
async def auth_apple(request: AppleAuthRequest, db: Session = Depends(get_db)):
    try:
        decoded = await verify_apple_token(request.id_token, request.nonce)
        apple_sub = decoded["sub"]
        now = datetime.now(timezone.utc)

        user = db.query(User).filter(User.apple_sub == apple_sub).first()

        if user:
            user.last_login = now

            updated_email = decoded.get("email") or request.email
            if updated_email and updated_email != user.email:
                user.email = updated_email

            verified_flag = decoded.get("email_verified", user.email_verified)
            if verified_flag != user.email_verified:
                user.email_verified = verified_flag

            if not user.full_name and request.full_name:
                user.full_name = request.full_name

        else:
            user = User(
                apple_sub=apple_sub,
                full_name=request.full_name or None,
                email=decoded.get("email", request.email),
                email_verified=decoded.get("email_verified", False),
                created_at=now,
                last_login=now
            )
            db.add(user)

        db.commit()
        db.refresh(user)

        access_token, access_token_expires_at = create_access_token(user)
        refresh_token, refresh_token_expires_at = create_refresh_token(user=user)

        return AppleSignInResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            access_token_expires_at=access_token_expires_at,  
            refresh_token_expires_at=refresh_token_expires_at,
            user_id=str(user.id),
            email=user.email,
            is_verified=user.email_verified
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/renew_access_token", response_model=AccessTokenResponse)
def renew_access_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    try:
        payload = decrypt_token(request.refresh_token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        access_token, access_token_expires_at = create_access_token(user=user)

        return AccessTokenRefreshResponse(
            access_token=access_token,
            access_token_expires_at=access_token_expires_at,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token decryption failed: {str(e)}")

@router.post("/renew_refresh_token", response_model=RefreshTokenResponse)
def renew_refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    try:
        payload = decrypt_token(request.refresh_token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        refresh_token, refresh_token_expires_at = create_refresh_token(user=user)

        return RefreshTokenResponse(    
            refresh_token=refresh_token,
            refresh_token_expires_at=refresh_token_expires_at,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token renewal failed: {str(e)}")