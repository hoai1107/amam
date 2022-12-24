from fastapi import APIRouter, Depends, HTTPException, Response, status
import sys,os
from pathlib import Path
sys.path.insert(0,os.path.join(Path(__file__).parents[1],"database_connection"))
sys.path.insert(0,os.path.join(Path(__file__).parents[1],"data_model"))
from db_connection import auth, auth_admin, mongodb
from user_model import UserDB, Account
from fastapi.security import OAuth2PasswordRequestForm
import smtplib
from email.message import EmailMessage
import ssl
from dependencies import oauth2_scheme

router = APIRouter(
    prefix= "/authentication",
    tags= ["Authentication"]
)

async def create_user(user: UserDB):
    try:
        user_dict = user.dict()
        current_user = mongodb["users"].insert_one(user_dict)
    except:
        return Response(status_code= status.HTTP_400_BAD_REQUEST, content="Something wrong!")
    # the Id of the user
    return str(current_user.inserted_id)

async def send_verification_to_mail(email_receiver: str):
    email_sender = 'quocthogminhqtm@gmail.com'
    email_password = "qjikpcbndhxofrvr"
    authentication_link = auth_admin.generate_email_verification_link(email=email_receiver)
    subject = "Account Verification"
    body= \
    """
Please access this link to authenticate the account: {}
    """.format(authentication_link)
    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_receiver
    em["Subject"] = subject
    em.set_content(body)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(email_sender,email_password)
        smtp.sendmail(email_sender,email_receiver, em.as_string())

#This is for signing up
# This is for the future need (can be changed)
@router.post("/sign-up")
async def sign_up(account: Account):
        email = account.email
        password = account.password
        user_name= account.user_name
        auth.create_user_with_email_and_password(email=email,password=password)
        user_id = auth.sign_in_with_email_and_password(email=email, password= password)["localId"]
        created_user =  UserDB(user_id=user_id,user_name=user_name, email=email)
        await create_user(created_user)
        await send_verification_to_mail(email_receiver=email)
        return {"user_id": user_id}

# This is to create the token
# email = user_name is due to the conflict between the specification and our app
# This just for future need (can be changed)
@router.post("/sign-in")
async def sign_in(signin_form: OAuth2PasswordRequestForm = Depends()):
    email = signin_form.username
    password = signin_form.password
    try:
        user = auth.sign_in_with_email_and_password(email=email, password= password)
        token = user["idToken"]
        if not auth.get_account_info(id_token=token)['users'][0]['emailVerified']:
            await send_verification_to_mail(email_receiver=email)
            return HTTPException(status_code=400, detail={'message':'Email needs to be verified first'})
    except:
        raise HTTPException(status_code= 400, detail={"message":"There is a problem in the process"})
    return {"access_token": token, "token_type": "bearer"}

async def authentication(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials. Maybe it's due to the expiration of token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        decode_token = auth_admin.verify_id_token(token)
        return decode_token["uid"]
    except:
        raise credentials_exception    

@router.get("/test_authentication")
async def test(token: str = Depends(authentication)):
    return token