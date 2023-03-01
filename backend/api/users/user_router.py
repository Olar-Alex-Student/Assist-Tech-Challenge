
from fastapi import APIRouter, HTTPException, status
from .models import NewUser
from ..database.cosmo_db import users_container

router = APIRouter()


@router.post("/users", tags=["users"])
async def create_new_user(new_user: NewUser):

    # Try to see if the user already exists
    query = "SELECT co.name, co.email FROM c co WHERE co.email = @email OR co.name = @name"
    params = [dict(name="@email", value=new_user.email),
              dict(name="@name", value=new_user.name)]

    results = users_container.query_items(query=query,
                                          parameters=params,
                                          enable_cross_partition_query=True,
                                          max_item_count=1)

    items = [item for item in results]

    # If this is not empty, then a user with that name or email exists
    if items:
        existing_user = items[0]
        if existing_user['name'] == new_user.name:
            detail = f"User with the name '{new_user.name}' already exists."
        else:
            detail = f"User with the email '{new_user.email}' already exists."

        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)

    # No need to create a UUID, since the account name is unique
    # But cosmo DB NoSQL required all items to have an id key
    # I could store the name inside id, and then change id to name before sending the response, to avoid duplicate data
    # But I like it more this way for this "small" project, since it's not really a production app
    new_item = {'id': new_user.name, **new_user.dict()}

    users_container.create_item(new_item)

    return new_item


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
