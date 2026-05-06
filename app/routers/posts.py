from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# ─── CREATE ──────────────────────
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PostResponse
)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_post = models.Post(
        owner_id=current_user.id,
        **post.dict()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# ─── GET ALL ─────────────────────
@router.get(
    "/",
    response_model=List[schemas.PostResponse]
)
def get_all_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)
    ).limit(limit).offset(skip).all()

    return posts


# ─── GET ONE ─────────────────────
@router.get(
    "/{post_id}",
    response_model=schemas.PostResponse
)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(
        models.Post.id == post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID={post_id} bo'lgan post topilmadi"
        )

    return post


# ─── UPDATE ───────────────────────
@router.put(
    "/{post_id}",
    response_model=schemas.PostResponse
)
def update_post(
    post_id: int,
    updated_post: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    post_query = db.query(models.Post).filter(
        models.Post.id == post_id
    )
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post topilmadi"
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Siz bu postni o'zgartira olmaysiz"
        )

    post_query.update(
        updated_post.dict(exclude_unset=True),
        synchronize_session=False
    )

    db.commit()
    return post_query.first()


# ─── DELETE ───────────────────────
@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    post_query = db.query(models.Post).filter(
        models.Post.id == post_id
    )
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post topilmadi"
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Siz bu postni o'chira olmaysiz"
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    return None