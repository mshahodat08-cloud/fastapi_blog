from fastapi import APIRouter, HTTPException
from app.schemas import Category

router = APIRouter(prefix="/categories", tags=["Categories"])

categories_db = []
category_id = 1


# CREATE
@router.post("/")
def create_category(category: Category):
    global category_id

    cat = category.dict()
    cat["id"] = category_id
    category_id += 1

    categories_db.append(cat)
    return cat


# READ ALL
@router.get("/")
def get_categories():
    return categories_db


# READ ONE
@router.get("/{cat_id}")
def get_category(cat_id: int):
    for c in categories_db:
        if c["id"] == cat_id:
            return c
    raise HTTPException(status_code=404, detail="Topilmadi")


# UPDATE
@router.put("/{cat_id}")
def update_category(cat_id: int, category: Category):
    for i, c in enumerate(categories_db):
        if c["id"] == cat_id:
            updated = category.dict()
            updated["id"] = cat_id
            categories_db[i] = updated
            return updated

    raise HTTPException(status_code=404, detail="Topilmadi")


# DELETE
@router.delete("/{cat_id}")
def delete_category(cat_id: int):
    for i, c in enumerate(categories_db):
        if c["id"] == cat_id:
            categories_db.pop(i)
            return {"xabar": "O'chirildi"}

    raise HTTPException(status_code=404, detail="Topilmadi")