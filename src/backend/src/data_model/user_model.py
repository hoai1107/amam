from pydantic import BaseModel, Field
from typing import Union
from fastapi import Path
from bson.objectid import ObjectId
from post_model import PostBase, PyObjectId

# This is a base unit model just holding small enough information
class UserBase(BaseModel):
    id: Union[PyObjectId,None] = Field(default_factory=PyObjectId,alias="_id")
    user_id: str
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Voting(BaseModel):
    id: str
    upvote_downvote: str 

# This is the main model of user holding full information of that user
class User(UserBase):
    user_name: str
    email: str
    avatar: str = Field(default=None)
    list_of_user_question: list[PostBase] = Field(default=list[PostBase]())
    list_of_post_voted: list[Voting] = Field(default= list[Voting]())
    list_of_comment_voted: list[Voting] = Field(default=list[Voting]())
    list_of_user_comments_id: list[str] = Field(default=list[str]())
    number_of_answer: int = 0
    list_of_followed: list[UserBase] = Field(default=list[UserBase]())
    bookmark: list[PostBase] = Field(default=list[PostBase]())
    history_posts: list[PostBase] = Field(default= list[PostBase]())

# This plays a role as the model for creating data to the database
class UserDB(BaseModel):
    user_id: str
    user_name: str
    email: str
    avatar: str = Field(default=None)
    list_of_user_question: list[PostBase] = Field(default=list[PostBase]())
    list_of_post_voted: list[Voting] = Field(default= list[Voting]())
    list_of_comment_voted: list[Voting] = Field(default=list[Voting]())
    list_of_user_comments_id: list[str] = Field(default=list[str]())
    number_of_answer: int = 0
    list_of_followed: list[UserBase] = Field(default=list[UserBase]())
    bookmark: list[PostBase] = Field(default=list[PostBase]())
    history_posts: list[PostBase] = Field(default= list[PostBase]())

# This is the form of information used in the authentication process 
class Account(BaseModel):
    user_name: str
    email: str
    password: str = Path(min_length=6)
