from pydantic import BaseModel
import datetime
from fastapi import Path
from typing import Union

class UserBase(BaseModel):
    id: Union[str,None] = None
    user_name: str
    email: str

class PostBase(BaseModel):
    id: Union[str,None] = None
    title: str

class VotingUser(UserBase):
    upvote_downvote: str 

class Comments(BaseModel):
    id: str
    user_id: str
    is_deleted: bool = False
    content_of_comment: str
    upvote: int
    downvote: int
    list_of_user_upvote_downvote_cmt: Union[list[VotingUser],None] = None 

class Post(PostBase):
    view: int = 0
    time_create: datetime.date
    tags: Union[None,list[str]] = None
    upvote: int = 0
    downvote: int = 0
    comments: Union[list[Comments],None] = None
    list_of_user_upvote_downvote: Union[list[VotingUser],None] = None
    list_of_user_see_post: Union[list[UserBase],None] = None

class User(UserBase):
    avatar: Union[str,None] = None
    list_of_user_question: Union[list[PostBase],None] = None
    number_of_answer: int = 0
    list_of_followed: Union[list[UserBase],None] = None

class Account(BaseModel):
    user_name: str
    email: str
    password: str = Path(min_length=6)