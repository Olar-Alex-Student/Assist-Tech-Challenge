from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from backend.api.users import user_router

description = """
The Bizonii backend API. 🐂

## Users

* You can **GET** the data of **one user**.
* You can **GET** the data of **multiple users**.
* You can **POST** to create **new users**.
* You can **POST** to create **new users**.
* You can **DELETE** an existing **user**.

## Forms

* _NOT IMPLEMENTED_
"""

app = FastAPI(
    title="Bizonii Backend",
    description=description,
    version="0.0.0",
    license_info={
        "name": "CC0",
        "url": "https://creativecommons.org/publicdomain/zero/1.0/"},
    contact={
        "name": "Vizitiu Valentin",
        "email": "vizitiuvalentin12@gmail.com"}
)

app.include_router(user_router.router)


@app.get("/", include_in_schema=False)
async def send_to_docs() -> RedirectResponse:
    # Since the url for the backend is different from the frontend, if the user accesses the base url, redirect them
    # to the docs page directly

    return RedirectResponse(url="./docs")
