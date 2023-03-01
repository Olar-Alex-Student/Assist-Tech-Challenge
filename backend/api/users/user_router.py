"""
Author: Vizitiu Valentin Iulian
License: CC0 “No Rights Reserved”
Link: https://creativecommons.org/publicdomain/zero/1.0/

You are free to copy, modify and use the code in any way. I am not res
"""

from fastapi import APIRouter, HTTPException, Path, Body, status
from .models import NewUser, UpdatedUser, UserLogin
from .functions import get_user_by_email_or_name
from ..database.cosmo_db import users_container

import azure

router = APIRouter()


@router.post(path="/users/login/:{unique_identifier}",
             tags=["users"],
             description="Provide the user password to log into the account.")
async def login_user(
        user_login: UserLogin,
        unique_identifier: str = Path(default="Valentin",
                                      title="An unique identifier to search the user by.",
                                      description="The email or name of the user.")):
    user = get_user_by_email_or_name(account_name=unique_identifier,
                                     email=unique_identifier)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    current_user = users_container.read_item(
        item=user['name'],
        partition_key=user['name'],
    )

    # This can be improved by adding some token authentication method like JWT Token|
    # Can update if there is time
    if current_user['password'] != user_login.password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong password.")

    # Return the 200 status code
    return


@router.post(path="/users",
             tags=["users"],
             description="Create a new user.")
async def create_new_user(
        new_user: NewUser = Body(description="A JSON with the initial user data. All fields are "
                                             "mandatory, except fiscal code, only companies should have this.")):
    # Try to see if the user already exists
    user = get_user_by_email_or_name(email=new_user.email,
                                     account_name=new_user.name)

    # If this is not empty, then a user with that name or email exists
    if user:
        if user['name'] == new_user.name:
            detail = f"User with the name '{new_user.name}' already exists."
        else:
            detail = f"User with the email '{new_user.email}' already exists."

        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)

    # Cannot set fiscal code for individual accounts
    if new_user.fiscal_code and new_user.account_type == 'individual':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot set 'fiscal code' for individuals.")

    # No need to create a UUID, since the account name is unique
    # But cosmo DB NoSQL required all items to have an id key
    # I could store the name inside id, and then change id to name before sending the response, to avoid duplicate data
    # But I like it more this way for this "small" project, since it's not really a production app
    new_item = {'id': new_user.name, **new_user.dict()}

    users_container.create_item(new_item)

    return new_item


@router.get(path="/users/:{unique_identifier}",
            tags=["users"],
            description="Get all the data about one user.")
async def get_one_user(
        unique_identifier: str = Path(default="Valentin",
                                      example="Vizitiu Valentin",
                                      title="An unique identifier to search the user by.",
                                      description="The email or name of the user.")):
    user = get_user_by_email_or_name(account_name=unique_identifier,
                                     email=unique_identifier)

    # Raise 404 if there are 0 results
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    return user


@router.put(path="/users/:{account_name}",
            tags=["users"],
            description="Update any of the user fields. In the body give only the values you wish to update.")
async def update_user(
        updated_user: UpdatedUser,
        account_name: str = Path(example="Vizitiu Valentin",
                                 description="The name of the account to delete.")) -> UpdatedUser:
    # Verify if the user exists
    # Here we can use the read_item method since we are sure we have the account name
    try:
        current_user = users_container.read_item(
            item=account_name,
            partition_key=account_name,
        )
    except azure.cosmos.exceptions.CosmosResourceNotFoundError:  # type: ignore
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    # Cannot change account type
    if current_user['account_type'] != updated_user.account_type:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="'account type' field cannot be updated.")

    # Cannot set fiscal code for individual accounts
    if updated_user.fiscal_code and current_user['account_type'] == 'individual':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot set 'fiscal code' for individuals.")

    # Cannot update account name
    print(updated_user.name, current_user['name'])
    if updated_user.name != current_user['name']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="'account name' field cannot be updated.")

    print(updated_user.email, current_user['email'])
    updated_email = updated_user.email != current_user['email']

    # If they modified the email or account name, check if one already exists
    if updated_email:
        user = get_user_by_email_or_name(account_name=updated_user.name,
                                         email=updated_user.email)

        if user:
            detail = f"User with the email '{updated_user.email}' already exists."
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)

    # We can create the updated user
    new_user = {'password': current_user['password'],
                'id': current_user['name'],
                **updated_user.dict()}

    # Now we can save the updated data
    users_container.upsert_item(new_user)

    return updated_user


@router.delete(path="/users/:{account_name}",
               tags=["users"],
               description="Delete one user from the database.")
async def delete_user(
        account_name: str = Path(example="Vizitiu Valentin",
                                 description="The name of the account to delete.")) -> None:
    # We will always have the account name when we want to delete an item
    # Cosmo DB NoSql provides only this way to delete items, so we can't use the email too
    # Only with an extra query
    try:
        users_container.delete_item(
            item=account_name,
            partition_key=account_name,
        )
    except azure.cosmos.exceptions.CosmosResourceNotFoundError:  # type: ignore
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
