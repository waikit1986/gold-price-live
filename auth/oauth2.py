from fastapi import Depends, HTTPException, status
from fastapi import Security
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from db.database import get_db
from datetime import datetime, timezone

from auth.tokens import decrypt_token
from user.models_user import User

auth_scheme = HTTPBearer()


def get_current_user(
    token: HTTPAuthorizationCredentials = Security(auth_scheme),
    db: Session = Depends(get_db)
):
    try:
        token_str = token.credentials

        payload = decrypt_token(token_str)

        type = payload.get("type")
        if type != "access_token":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token type not access token")

        exp = payload.get("exp")
        if exp is None or datetime.now(timezone.utc).timestamp() > exp:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")

        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID not found in token")

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
