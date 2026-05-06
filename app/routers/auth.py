from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError


from .. import models, schemas
from ..database import get_db
from ..utils.hashing import verify_password
from ..oauth2 import create_access_token, create_refresh_token
from ..config import settings
from .. import models, schemas
from ..database import get_db
from ..utils.hashing import verify_password, hash_password
from ..oauth2 import get_current_user

router = APIRouter(tags=["Authentication"])


# ───────── LOGIN ─────────
@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Noto'g'ri email yoki parol"
        )

    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Noto'g'ri email yoki parol"
        )

    access_token = create_access_token(data={"user_id": user.id})
    refresh_token = create_refresh_token(data={"user_id": user.id})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# ───────── REFRESH ─────────
@router.post("/refresh")
def refresh_token(request: schemas.RefreshTokenRequest):
    try:
        payload = jwt.decode(
            request.refresh_token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )

        user_id = payload.get("user_id")
        token_type = payload.get("type")

        if user_id is None or token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        new_access_token = create_access_token(
            data={"user_id": user_id}
        )

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Token expired or invalid")
    

@router.post("/logout")
def logout():
    return {
        "message": "Logout successful. Tokenni client o‘chirishi kerak."
    }