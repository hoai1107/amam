from fastapi import APIRouter, Response, status, Depends ,HTTPException
from ..database_connection.test_firebase_connection import db, auth
from ..data_model.user_model import User

router = APIRouter(
    prefix="/users",
    tags= ["Users"]
)

# This is to get all information related to a specific user
@router.get("/user_info/{user_id}", response_model= User)
async def get_user(user_id: str):
    try:    
        current_user = db.child("users").child(user_id).get().val()
        profile_user_model = User(**(current_user))
        profile_user_model.id = user_id
    except:
        return Response(status_code= status.HTTP_400_BAD_REQUEST, content="Something wrong!") 
    return profile_user_model

# This is to create the a user information (and get the ID of the user)
@router.put("/user_info/")
async def create_user(user: User):
    try:
        user_dict = user.dict()
        del user_dict["id"]
        current_user = db.child("users").push(user_dict)
    except:
        return Response(status_code= status.HTTP_400_BAD_REQUEST, content="Something wrong!")
    # the Id of the user
    return current_user["name"]

