from fastapi import APIRouter, Depends, HTTPException
from ..database_connection.test_firebase_connection import  auth
from ..data_model.user_model import User, Account
from fastapi.security import OAuth2PasswordRequestForm
from user import post_user_profile

router = APIRouter(
    tags= ["Authentication"]
)

#This is for signing up
# This is for the future need (can be changed)
@router.post("/Signup")
async def sign_up(account: Account = Depends()):
    email = account.email
    password = account.password
    user_name= account.user_name
    created_user =  User(user_name=user_name, email=email)
    try:
        auth.create_user_with_email_and_password(email=email,password=password)
        created_user_id = await post_user_profile(created_user)
    except:
        raise HTTPException(status_code= 400, detail={"message":"There is a problem in the process"})
    return created_user_id

# This is to create the token
# email = user_name is due to the conflict between the specification and our app
# This just for future need (can be changed)
@router.post("/Signin")
async def sign_in(signin_form: OAuth2PasswordRequestForm = Depends()):
    email = signin_form.username
    password = signin_form.password
    try:
        user = auth.sign_in_with_email_and_password(email=email, password= password)
        token = user["idToken"]
        if not auth().get_account_info(id_token=token)['users'][0]['emailVerified']:
            raise  HTTPException(status_code=400, detail={'message':'Email needs to be verified first'})
        return {"access_token": token, "token_type": "bearer"}
    except:
        raise HTTPException(status_code=400, detail={"message": "There is a problem in the process!"})