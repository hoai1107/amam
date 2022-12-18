from pydantic import BaseModel, Field
import datetime
from typing import Union
from bson.objectid import ObjectId
from enum import Enum

class PyObjectId(ObjectId):
    """ Custom Type for reading MongoDB IDs """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid object_id")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class PostBase(BaseModel):
    id: Union[PyObjectId,None] = Field(default_factory=PyObjectId,alias="_id")
    title: str
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

from user_model import VotingUser

# This model plays a role as a model in the architecture
class CommentDB(BaseModel):
    user_id: str
    post_id: str
    is_root_comment: bool = Field(default= True)
    content_of_comment: str
    up_vote: int
    down_vote: int
    list_child_comment_id: list[str] = Field(default= list[str]())
    list_of_user_upvote_downvote_cmt: list[VotingUser]= Field(default=list[VotingUser]())

# This model plays a role as a view in the architecture
class Comments(CommentDB):
    id: Union[PyObjectId,None] = Field(default_factory=PyObjectId,alias="_id")
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# This model plays a role as a view in the architecture
class ShortPost(PostBase):
    view: int = Field(default=0)
    time_created: datetime.datetime
    content: str = Field(default="")
    tags: list[str] = Field(default=list[str]())
    up_vote: int = Field(default=0)
    down_vote: int = Field(default=0)
    num_comments: int = Field(default=0)

# This model plays a role as a view in the architecture
class FullPost(ShortPost):
    user_id: str
    avatar: str = Field(default= None)
    list_of_user_upvote_downvote: list[VotingUser] = Field(default=list[VotingUser]())

# This model plays a role as a model in the architecture
class PostDB(BaseModel):
    user_id: str
    title: str
    content: str = Field(default="")
    view: int = Field(default=0)
    time_created: datetime.datetime
    tags: list[str] = Field(default=list[str]())
    up_vote: int = Field(default=0)
    down_vote: int = Field(default=0)
    num_comments: int = Field(default=0)
    list_of_user_upvote_downvote: list[VotingUser] = Field(default=list[VotingUser]())
    
# This will be refined in the future when the frontend is fullfiled
class SearchFilter(str,Enum):
    all = "all"
    technology = "technology"
    math = "math"

class OrderByOption(str,Enum):
    default = "default"
    comment = "comment"
    view = "view"
    vote = "vote"

    
 