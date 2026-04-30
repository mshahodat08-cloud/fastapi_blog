from fastapi import FastAPI
from app.routers import posts, category
from app.routers import todo


app = FastAPI(
    title="Blog API",
    description="FastAPI bilan yaratilgan Blog API",
    version="1.0.0"
)

# Routers
app.include_router(posts.router)
app.include_router(category.router)
app.include_router(todo.router)


@app.get("/")
def root():
    return {"xabar": "Blog API ga xush kelibsiz!"}