from pydantic import BaseModel, Field, validator
import datetime
from typing import Union

class UserBase(BaseModel):
    user_id: Union[str,None] = None
    user_name: str

class PostBase(BaseModel):
    post_id: Union[str,None] = None
    title: str

class User(UserBase):
    avartar: Union[str,None] = None
    list_of_user_question: Union[list[PostBase],None] = None
    number_of_answer: int = 0
    list_of_followed: Union[list[UserBase],None] = None

class VotingUser(UserBase):
    upvote_downvote: str 

class Comments(BaseModel):
    comment_id: str
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







