from fastapi import APIRouter, Depends, HTTPException, Response
from ..database_connection.db_connection import auth, auth_admin
from ..data_model.user_model import User, Account
from fastapi.security import OAuth2PasswordRequestForm
from .user import create_user
import smtplib
from email.message import EmailMessage
import ssl

router = APIRouter(
    tags= ["Authentication"]
)

#This is for signing up
# This is for the future need (can be changed)
@router.post("/sign-up")
async def sign_up(account: Account = Depends()):
    email = account.email
    password = account.password
    user_name= account.user_name
    created_user =  User(user_name=user_name, email=email)
    try:
        auth.create_user_with_email_and_password(email=email,password=password)
        created_user_id = await create_user(created_user)
    except:
        return HTTPException(status_code= 400, detail={"message":"There is a problem in the process"})
    return {"user_id": created_user_id, "email_verification_link": auth_admin.generate_email_verification_link(email=email)}

async def send_verification_to_mail(email_receiver: str):
    email_sender = 'quocthogminhqtm@gmail.com'
    email_password = "qjikpcbndhxofrvr"
    authentication_link = auth_admin.generate_email_verification_link(email=email_receiver)
    subject = "Please Verify Your Email in AMAM APP With The Given Link :)))"
    body= \
    """
    This is a test e-mail message.
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