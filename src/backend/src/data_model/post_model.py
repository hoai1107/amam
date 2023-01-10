from pydantic import BaseModel, Field
import datetime
from typing import Union
from bson.objectid import ObjectId
from enum import Enum
import pytz

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

# This model plays a role as a model in the architecture
class CommentDB(BaseModel):
    post_id: str
    root_comment_id: str = Field(default= "root")
    time_created: datetime.datetime = Field(default= datetime.datetime.now(pytz.UTC))
    user_id: str = Field(default=None)
    content: str
    upvote: int = Field(default=0)
    downvote: int = Field(default=0)
    list_child_comment_id: list[str] = Field(default= list[str]())

# This model plays a role as a view in the architecture
class CommentBase(BaseModel):
    id: Union[PyObjectId,None] = Field(default_factory=PyObjectId,alias="_id")
    time_created: str
    user_id: str
    user_name: str = Field(default=None)
    user_avatar: str = Field(default=None)
    post_id: str
    root_comment_id: str = Field(default= "root")
    content: str
    upvote: int = Field(default=0)
    downvote: int = Field(default=0)
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Comments(CommentBase):
    list_child_comment: list[CommentBase] = Field(default= list[CommentBase]())

# This model plays a role as a view in the architecture
class Posts(PostBase):
    user_id: str = Field(default= None)
    view: int = Field(default=0)
    time_created: str
    content: str = Field(default="")
    tags: list[str] = Field(default=list[str]())
    upvote: int = Field(default=0)
    downvote: int = Field(default=0)
    num_comments: int = Field(default=0)

# This model plays a role as a model in the architecture
class PostDB(BaseModel):
    user_id: str = Field(default= None)
    title: str
    content: str = Field(default="")
    view: int = Field(default=0)
    time_created: datetime.datetime = Field(default= datetime.datetime.now(pytz.UTC))
    tags: list[str] = Field(default=list[str]())
    upvote: int = Field(default=0)
    downvote: int = Field(default=0)
    num_comments: int = Field(default=0)
    list_user_view_id: list[int] = Field(default=list[int]())

# This will be refined in the future when the frontend is fullfiled
class SearchFilter(str,Enum):
    all = "All"
    business = "Business"
    cooking = "Cooking"
    design = "Design"
    economics = "Economics"
    education = "Education"
    fastion_style = "Fashion & Style"
    finance = "Finance"
    fine_art = "Fine Art"
    food = "Food"
    health = "Health"
    history = "History"
    journalism = "Journalism"
    literature = "Literature"
    marketing = "Marketing"
    mathematics = "Mathematics"
    movies = "Movies"
    music = "Music"
    philosophy = "Philosophy"
    politics = "Politics"
    psycology = "Psycology"
    sience = "Science"
    sports = "Sports"
    technology = "Technology"
    travel = "Travel"
    writing = "Writing"
    others = "Others"

class OrderByOption(str,Enum):
    default = "default"
    comment = "comment"
    view = "view"
    vote = "vote"
 