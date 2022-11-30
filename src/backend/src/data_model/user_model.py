from pydantic import BaseModel
from typing import Union
from fastapi import Path
from .post_model import PostBase

class UserBase(BaseModel):
    id: Union[str,None] = None
    user_name: str
    email: str

class VotingUser(UserBase):
    upvote_downvote: str 

class User(UserBase):
    avatar: Union[str,None] = None
    list_of_user_question: Union[list[PostBase],None] = None
    number_of_answer: int = 0
    list_of_followed: Union[list[UserBase],None] = None

class Account(BaseModel):
    user_name: str
    email: str
    password: str = Path(min_length=6)
