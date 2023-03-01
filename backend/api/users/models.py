"""
Check the links I provided to learn more about WHY I did something in that way
"""

from pydantic import BaseModel
from fastapi import Path
from enum import Enum


# https://fastapi.tiangolo.com/tutorial/path-params/#create-an-enum-class
class AccountType(str, Enum):
    individual = "individual"
    company = "company"
    public_institution = "public_institution"


class UserLogin(BaseModel):
    password: str

    class Config:
        schema_extra = {
            "example": {
                "password": "supersecretpassword"
            }
        }


class NewUser(BaseModel):
    account_type: AccountType
    name: str = Path(default="Poggers")
    fiscal_code: str = None
    address: str
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Vizitiu Valentin",
                "email": "poggers1234@pogmail.com",
                "account_type": AccountType.individual.value,
                "address": "7353 South St. Braintree, MA 02184",
                "fiscal_code": "",
                "password": "supersecretpassword"
            }
        }


class UpdatedUser(BaseModel):
    """
    Represents the updated user.
    This doesn't include the password.
    """
    account_type: AccountType
    name: str = Path(default="Poggers")
    fiscal_code: str = None
    address: str
    email: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Vizitiu Valentin",
                "email": "poggers1234@pogmail.com",
                "account_type": AccountType.individual.value,
                "address": "7353 South St. Braintree, MA 02184",
                "fiscal_code": "",
            }
        }


