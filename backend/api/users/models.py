"""
Check the links I provided to learn more about WHY I did something in that way
"""

from pydantic import BaseModel
from enum import Enum


# https://fastapi.tiangolo.com/tutorial/path-params/#create-an-enum-class
class AccountType(str, Enum):
    individual = "individual"
    company = "company"
    public_institution = "public_institution"


class NewUser(BaseModel):
    account_type: AccountType
    name: str
    fiscal_code: str = None
    address: str
    email: str
    password: str


