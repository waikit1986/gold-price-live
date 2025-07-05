from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from user.models_user import User
from . import functions_user
from auth.oauth2 import get_current_user


router = APIRouter(
    prefix='/user',
    tags=['User'],
)


@router.delete('', response_model=str)
def delete_user(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return functions_user.delete_user(db, user)