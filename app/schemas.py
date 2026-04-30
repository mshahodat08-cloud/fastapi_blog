from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel
from pydantic import BaseModel, EmailStr, validator


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


class Category(BaseModel):
    name: str
    description: str


class Todo(BaseModel):
    title: str
    completed: bool = False


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Parol kamida 8 ta belgi bo'lishi kerak")
        return v