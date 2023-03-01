from fastapi import APIRouter

router = APIRouter()


@router.post("/users", tags=["users"])
async def create_new_user():
    pass


@router.get("/users", tags=["users"])
async def get_one_user():
    pass


@router.get("/users", tags=["users"])
async def get_users():
    pass


@router.put("/users", tags=["users"])
async def update_user():
    pass


@router.delete("/users", tags=["users"])
async def delete_user():
    pass


