from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    username: str
    email: str

@app.post("/users", response_model=UserResponse)
def create_user(user: User):
    return user  

@app.get("/")
def read_root():
    return {"xabar": "Salom FastAPI!"}


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


posts_db = []
post_id_counter = 1



class PostNotFound(Exception):
    pass



@app.exception_handler(PostNotFound)
async def post_not_found_handler(request: Request, exc: PostNotFound):
    return JSONResponse(
        status_code=404,
        content={
            "xato": "Post topilmadi",
            "tavsiya": "Boshqa ID ni sinab ko'ring"
        }
    )


# CREATE
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    global post_id_counter

    post_dict = post.dict()
    post_dict["id"] = post_id_counter
    post_id_counter += 1

    posts_db.append(post_dict)

    return {"xabar": "Post yaratildi", "post": post_dict}


# READ ALL
@app.get("/posts")
def get_all_posts():
    return {"posts": posts_db}


# READ ONE ✅ (FAKAT BITTA QOLDI)
@app.get("/posts/{post_id}")
def get_post(post_id: int):
    for post in posts_db:
        if post["id"] == post_id:
            return {"post": post}

    raise PostNotFound()


# UPDATE
@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    for index, p in enumerate(posts_db):
        if p["id"] == post_id:
            post_dict = post.dict()
            post_dict["id"] = post_id
            posts_db[index] = post_dict
            return {"xabar": "Post yangilandi", "post": post_dict}

    raise PostNotFound()


# DELETE
@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    for index, post in enumerate(posts_db):
        if post["id"] == post_id:
            posts_db.pop(index)
            return {"xabar": "Post o'chirildi"}

    raise PostNotFound()