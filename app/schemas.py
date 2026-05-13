from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from app.models import Category


# ─────────────────────────────
# 🟡 USER SCHEMAS
# ─────────────────────────────

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Parol kamida 8 ta belgi bo'lishi kerak")
        return v


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ─────────────────────────────
# 🔐 AUTH SCHEMAS
# ─────────────────────────────

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
    token_type: Optional[str] = None  # access / refresh


class RefreshTokenRequest(BaseModel):
    refresh_token: str


# ─────────────────────────────
# 🔑 PASSWORD SCHEMA
# ─────────────────────────────

class PasswordChange(BaseModel):
    old_password: str
    new_password: str


# ─────────────────────────────
# 🟢 POST SCHEMAS
# ─────────────────────────────

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None 
    category_id: Optional[int] = None


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None

class OwnerInfo(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: Optional[int] = None
    owner: Optional[OwnerInfo] = None   # ← YANGI

    class Config:
        from_attributes = True

# ─────────────────────────────
# 🟣 CATEGORY SCHEMAS
# ─────────────────────────────

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CategoryOut(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PostOut(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    category: Optional[CategoryOut] = None 

    class Config:
        from_attributes = True
# ─────────────────────────────
# 🔵 TODO (optional)
# ─────────────────────────────

class Todo(BaseModel):
    title: str
    completed: bool = False





class RefreshTokenRequest(BaseModel):
    refresh_token: str

class PasswordChange(BaseModel):
    old_password: str
    new_password: str