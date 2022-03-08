from typing import Optional

from zark.schemas.base import Schema, JSONSchema


class User(JSONSchema):

    first_name: str
    last_name: str
    email: str
    age: Optional[int]

