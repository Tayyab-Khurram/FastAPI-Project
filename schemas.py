# in this file, we are going to define the type of the data
# that we want to accept and return from our API endpoints

# yeh wali file data ki rule book hai - yahan pay hum batayeein gay
# kis tarha ka data andar aaye ga aur kis tarha ka bahir jaaye ga.

from pydantic import BaseModel

class CreatePost(BaseModel):
    rating: int
    title: str
    review_text: str
    reviewer: str
    date: str
