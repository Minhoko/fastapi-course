from os import stat
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from schemas.user import UserBase, ShowUser
from models.users import User
from config.hashing import get_password_hash
from db.session import get_db

router = APIRouter(tags=["Users"])


@router.post("/register", response_model=ShowUser)
def create_user(user: UserBase, db: Session = Depends(get_db)):
    try:
        hashed_password = get_password_hash(user.password)
        new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
        db.add(new_user)
        db.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="This user already exists"
        )

    db.refresh(new_user)
    return new_user
