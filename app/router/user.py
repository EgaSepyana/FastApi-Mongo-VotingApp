from datetime import datetime
from typing import List
import os
from email.message import EmailMessage
import ssl
import smtplib
from fastapi import APIRouter , Depends , HTTPException , status
from .. import database
from .. import schema
from .. import utils
from .. import Oauth2

router = APIRouter(
    tags=["Users"]
)

@router.post("/users" , response_model=schema.userOut)
async def create_user(user:schema.Users, Current_user:dict = Depends(Oauth2.get_current_user)):
    role_list = ["admin", "user"]
    user_role = user.role.lower()
    role = Current_user.get("role")

    check_user_aleredy_exist = await database.get_user_by_email(user.email)

    if role == "user":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only Admin and super_admin can add a user")

    if (role == "admin") & ((user_role == "admin") | (user_role == "super_admin")):
        if user_role == "super_admin":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Cannot make a super_admin") 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only super_admin can Create Admin")

    if user_role not in role_list:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="only can insert role ('admin', 'user)")

    if check_user_aleredy_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email Already Exist")

    user = user.dict()
    user["password"] = utils.hash(user["password"])
    data = await database.create_user(user)
    return data

@router.get("/users", response_model=List[schema.userOut])
async def get_all_user(Current_user:dict = Depends(Oauth2.get_current_user)):
    is_active = Current_user.get("is_active")
    if not is_active:
       raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE , detail="Your Has disable for this request")
    return await database.get_all_user()

@router.put("/users/{email}", response_model=schema.userOut)
async def disable_user(email:str, data:schema.diable_user,Current_user:dict = Depends(Oauth2.get_current_user)):
    role = Current_user.get("role")

    user_data = await database.get_user_by_email(email)

    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not exist")

    user_role = user_data.get("role")

    if role == "user":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only Admin and super_admin can make user disable or not disable")

    if (role == "admin") & ((user_role == "admin") | (user_role == "super_admin")):
        if user_role == "super_admin":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Cannot make a super_admin Disable or not disable") 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only super_admin can make admin Disable or not disable")
    

    new_data = await database.disable_user(email=email, data=data.dict())

    return new_data

@router.put('/change_password')
async def change_password(pasword:schema.Change_password ,Current_user:dict = Depends(Oauth2.get_current_user)):
    user_data = await database.get_user_by_id(Current_user.get("_id"))

    if not utils.verify(plain_password=pasword.old_password , hashed_password=user_data.get("password")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Wrong Old password")

    new_password = utils.hash(password=pasword.new_password)    

    await database.update_user_password(password=new_password ,email=user_data.get("email"))

    return {"Massage" : "password changed"}

@router.post("/forget_password")
async def forget_password(active_user_email:schema.Gmail_user):
    verif_code = await database.add_verif_code()
    verif_code = str(verif_code.get("_id"))
    try:
        email = os.getenv("EMAIL")
        email_password = os.getenv("EMAIL_APP_PASSWORD")
        email_rechiver = active_user_email.your_active_gmail

        subject = "Your Verification code"
        body =f"""Dont let people know your reset password verivication code \n\nYour Verification Code : {verif_code} \n\n This Code Has expire in 3 Minutes"""

        msg = EmailMessage()
        msg["From"] = "Voting App"
        msg["To"] = email_rechiver
        
        msg["Subject"] = subject
        msg.set_content(body)
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email, email_password)
            smtp.sendmail(email, email_rechiver , msg.as_string())
    
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Email Founded")

    return {"Massage" : "Verification code is Send to your Active Email"}

@router.post("/reset_password")
async def reset_password(verif_code:schema.verifycation_code):
    verification_code = await database.get_verif_code(verif_code=verif_code.verifycation_code)
    if not verification_code:
        return {"Massage" : "Wrong Verication code"}

    expire_code = verification_code.get("expire_code")

    if expire_code < datetime.utcnow():
        return {"massage" : "your verification code has expire"}

    return{"Massage" : "reset password succesful"}