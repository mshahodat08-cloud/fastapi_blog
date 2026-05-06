from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..utils.hashing import hash_password, verify_password
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# ─── CREATE USER ──────────────────────────────
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserResponse
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu email allaqachon ro'yxatdan o'tgan"
        )

    user_data = user.dict()
    user_data["password"] = hash_password(user.password)

    new_user = models.User(**user_data)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ─── GET USER BY ID ───────────────────────────
@router.get(
    "/{user_id}",
    response_model=schemas.UserResponse
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID={user_id} bo'lgan foydalanuvchi topilmadi"
        )

    return user


# ─── GET CURRENT USER (/me) ───────────────────
@router.get(
    "/me",
    response_model=schemas.UserResponse
)
def get_me(
    current_user: models.User = Depends(get_current_user)
):
    return current_user


# ─── CHANGE PASSWORD (/me/password) ───────────
@router.put("/me/password")
def change_password(
    passwords: schemas.PasswordChange,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if not verify_password(passwords.old_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Eski parol noto‘g‘ri"
        )
    hashed_password = hash_password(passwords.new_password)
    user_query = db.query(models.User).filter(
        models.User.id == current_user.id
    )

    user_query.update(
        {"password": hashed_password},
        synchronize_session=False
    )

    db.commit()

    return {"message": "Parol muvaffaqiyatli o‘zgartirildi"}