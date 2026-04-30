from fastapi import APIRouter, HTTPException
from app.schemas import Todo

router = APIRouter(prefix="/todos", tags=["Todos"])

todos_db = []
todo_id = 1


@router.post("/")
def create_todo(todo: Todo):
    """
    Yangi todo yaratish

    - todo: title va completed maydonlari

    Returns:
        Yaratilgan todo (id bilan)
    """

    global todo_id

    t = todo.dict()
    t["id"] = todo_id
    todo_id += 1

    todos_db.append(t)
    return t


@router.get("/")
def get_todos():
    """
    Barcha todoslarni olish

    Returns:
        todos list
    """
    return todos_db


@router.put("/{todo_id}")
def update_todo(todo_id: int, todo: Todo):
    """
    Todo ni yangilash

    - todo_id: yangilanadigan todo ID
    - todo: yangi ma'lumotlar

    Returns:
        Yangilangan todo
    """

    for i, t in enumerate(todos_db):
        if t["id"] == todo_id:
            updated = todo.dict()
            updated["id"] = todo_id
            todos_db[i] = updated
            return updated

    raise HTTPException(status_code=404, detail="Topilmadi")


@router.delete("/{todo_id}")
def delete_todo(todo_id: int):
    """
    Todo ni o'chirish

    - todo_id: o'chiriladigan todo ID

    Returns:
        Xabar (o'chirildi)
    """

    for i, t in enumerate(todos_db):
        if t["id"] == todo_id:
            todos_db.pop(i)
            return {"xabar": "O'chirildi"}

    raise HTTPException(status_code=404, detail="Topilmadi")