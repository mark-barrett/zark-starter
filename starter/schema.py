from typing import Optional

from pydantic import BaseModel


class ZarkSchema(BaseModel):
    pass


class User(ZarkSchema):
    first_name: str
    last_name: str
    email: str
    age: Optional[int]
