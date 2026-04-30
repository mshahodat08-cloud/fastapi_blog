from fastapi import APIRouter, status, HTTPException
from typing import List
from ..schemas import PostCreate, PostResponse

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

posts_db = []
post_id = 1

@router.get("/", response_model=List[PostResponse])
def get_posts():
    return posts_db

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostCreate):
    global post_id
    post_dict = post.dict()
    post_dict["id"] = post_id
    post_id += 1
    posts_db.append(post_dict)
    return post_dict

@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int):
    for post in posts_db:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post topilmadi")

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    for index, post in enumerate(posts_db):
        if post["id"] == post_id:
            posts_db.pop(index)
            return None
    raise HTTPException(status_code=404, detail="Post topilmadi")

@router.get("/search")
def search_posts(q: str):
    result = []

    for post in posts_db:
        if q.lower() in post["title"].lower() or q.lower() in post["content"].lower():
            result.append(post)

    return {
        "q": q,
        "result": result
    }

@router.get("/")
def get_posts(skip: int = 0, limit: int = 10):
    return posts_db[skip : skip + limit]