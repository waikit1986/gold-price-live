from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .models_user import User


def delete_user(db: Session, user: User):
  user = db.query(User).filter(User.id == user.id).first()
  
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
      detail=f'User with ID {user.id} not found')
    
  db.delete(user)
  db.commit()

  return f'User with ID {user.id} was deleted successfully'

