from pydantic import BaseModel, Field
from typing import Union
from fastapi import Path
from bson.objectid import ObjectId

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


# This is a base unit model just holding small enough information
class UserBase(BaseModel):
    id: Union[PyObjectId,None] = Field(default_factory=PyObjectId,alias="_id")
    user_name: str
    email: str
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# This is extended from the base model, used for holding information of user upvoting or downvoting
class VotingUser(UserBase):
    upvote_downvote: str 

from post_model import PostBase

# This is the main model of user holding full information of that user
class User(UserBase):
    avatar: str = Field(default=None)
    list_of_user_question: list[PostBase] = Field(default=list[PostBase]())
    number_of_answer: int = 0
    list_of_followed: list[UserBase] = Field(default=list[UserBase]())
    bookmark: list[PostBase] = Field(default=list[PostBase]())
    history_posts: list[PostBase] = Field(default= list[PostBase]())

# This plays a role as the model for creating data to the database
class UserDB(BaseModel):
    user_name: str
    email: str
    avatar: str = Field(default=None)
    list_of_user_question: list[PostBase] = Field(default=list[PostBase]())
    number_of_answer: int = 0
    list_of_followed: list[UserBase] = Field(default=list[UserBase]())
    bookmark: list[PostBase] = Field(default=list[PostBase]())
    history_posts: list[PostBase] = Field(default= list[PostBase]())

# This is the form of information used in the authentication process 
class Account(BaseModel):
    user_name: str
    email: str
    password: str = Path(min_length=6)
