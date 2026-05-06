from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

# ─── CREATE ─────────────────────────────
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.CategoryResponse
)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    new_category = models.Category(**category.dict())

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


# ─── READ ALL ───────────────────────────
@router.get(
    "/",
    response_model=List[schemas.CategoryResponse]
)
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()


# ─── READ ONE ───────────────────────────
@router.get(
    "/{category_id}",
    response_model=schemas.CategoryResponse
)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category topilmadi"
        )

    return category


# ─── UPDATE ─────────────────────────────
@router.put(
    "/{category_id}",
    response_model=schemas.CategoryResponse
)
def update_category(
    category_id: int,
    updated_category: schemas.CategoryUpdate,
    db: Session = Depends(get_db)
):
    category_query = db.query(models.Category).filter(models.Category.id == category_id)
    category = category_query.first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category topilmadi"
        )

    category_query.update(updated_category.dict(), synchronize_session=False)
    db.commit()

    return category_query.first()


# ─── DELETE ─────────────────────────────
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category_query = db.query(models.Category).filter(models.Category.id == category_id)
    category = category_query.first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category topilmadi"
        )

    category_query.delete(synchronize_session=False)
    db.commit()

    return None