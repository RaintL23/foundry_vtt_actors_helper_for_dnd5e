# mi_proyecto/endpoints/users.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/users/")
async def read_users():
    return [{"user_id": "alice"}, {"user_id": "bob"}]

@router.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
