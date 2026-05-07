from fastapi import FastAPI
from .database import engine
from . import models
from .routers import posts, users, auth, category


app = FastAPI(
    title="Blog API",
    description="FastAPI + PostgreSQL + JWT Auth",
    version="3.0.0"
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(category.router)

@app.get("/")
def root():
    return {"xabar": "Blog API v3.0 — JWT Auth bilan!"}
