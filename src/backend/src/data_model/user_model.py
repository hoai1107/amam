from pydantic import BaseModel
from typing import Union
from fastapi import Path

# This is a base unit model just holding small enough information
class UserBase(BaseModel):
    id: Union[str,None] = None
    user_name: str
    email: str

# This is extended from the base model, used for holding information of user upvoting or downvoting
class VotingUser(UserBase):
    upvote_downvote: str 

from .post_model import PostBase

# This is the main model of user holding full information of that user
class User(UserBase):
    avatar: Union[str,None] = None
    list_of_user_question: Union[list[PostBase],None] = None
    number_of_answer: int = 0
    list_of_followed: Union[list[UserBase],None] = None

# This is the form of information used in the authentication process 
class Account(BaseModel):
    user_name: str
    email: str
    password: str = Path(min_length=6)
