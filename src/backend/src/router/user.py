from fastapi import APIRouter, Response, status
from ..database.test_firebase_connection import db
from ..data_mode.model import User


router = APIRouter(
    prefix="/users",
    tags= ["Users"]
)

# Query 1 in the design schema (on Notion)
@router.get("/user_profile/{user_id}", response_model= User)
async def get_user_profile(user_id: str):
    current_user = db.child("users").child(user_id).get().val()
    profile_user_model = User(**(current_user))
    profile_user_model.user_id = user_id
    return profile_user_model

# post the user information to the firebase and return the id
@router.put("/user_profile/")
async def post_user_profile(user: User):
    try:
        user_dict = user.dict()
        del user_dict["user_id"]
        current_user = db.child("users").push(user_dict)
    except:
        return Response(status_code= status.HTTP_400_BAD_REQUEST, content="Something wrong!")
    # the Id of the user
    return current_user["name"]