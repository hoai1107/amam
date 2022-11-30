from pydantic import BaseModel
import datetime
from typing import Union

class PostBase(BaseModel):
    id: Union[str,None] = None
    title: str

from .user_model import VotingUser, UserBase

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
    time_created: datetime.date
    tags: Union[None,list[str]] = None
    upvote: int = 0
    downvote: int = 0
    comments: Union[list[Comments],None] = None
    list_of_user_upvote_downvote: Union[list[VotingUser],None] = None
    list_of_user_see_post: Union[list[UserBase],None] = None

class ShortPost(PostBase):
    view: int = 0
    time_created: datetime.date
    tags: Union[None,list[str]] = None
    up_vote: int = 0
    down_vote: int = 0
    num_comments: int = 0

    
 