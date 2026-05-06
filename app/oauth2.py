from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import models, schemas
from .database import get_db
from .config import settings
from datetime import datetime, timedelta
from jose import jwt
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# ─── TOKEN YARATISH ───────────────────────────
def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )

    return encoded_jwt


# ─── TOKENNI TEKSHIRISH ───────────────────────
def verify_access_token(
    token: str,
    credentials_exception
) -> schemas.TokenData:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )

        user_id = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

        token_data = schemas.TokenData(
            user_id=int(user_id)
        )

    except JWTError:
        raise credentials_exception

    return token_data


# ─── CURRENT USER ─────────────────────────────
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Tokenni tekshirib bo'lmadi",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(
        models.User.id == token_data.user_id
    ).first()

    if user is None:
        raise credentials_exception

    return user

def create_refresh_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(days=7)

    to_encode.update({
        "exp": expire,
        "type": "refresh"
    })

    return jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )