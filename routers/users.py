from datetime import timedelta
from os import stat
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from schemas.user import UserBase, ShowUser
from models.users import User
from config.hashing import get_password_hash
from config.auth import authenticate_user, create_access_token
from config.settings import settings
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


@router.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
