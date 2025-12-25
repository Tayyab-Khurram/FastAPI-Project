# in this file, we are going to define the type of the data
# that we want to accept and return from our API endpoints

# yeh wali file data ki rule book hai - yahan pay hum batayeein gay
# kis tarha ka data andar aaye ga aur kis tarha ka bahir jaaye ga.

from pydantic import BaseModel
from fastapi_users import schemas
import uuid

class CreatePost(BaseModel):
    rating: int
    title: str
    review_text: str
    reviewer: str
    date: str

class ReturnPost(BaseModel):
    submitted: bool
    rating: int
    title: str
    review_text: str
    date: str

class UserCreate(schemas.BaseUserCreate):
    pass

class UserRead(schemas.BaseUser[uuid.UUID]):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass