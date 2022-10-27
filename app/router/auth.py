from fastapi import APIRouter , HTTPException , status , Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database
from .. import utils
from .. import Oauth2
from .. import schema

router = APIRouter(tags=["Auth"])

@router.post("/login", response_model=schema.Token)
async def login(credential_user: OAuth2PasswordRequestForm = Depends()):
    user = await database.get_user_by_email(email=credential_user.username)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not utils.verify(credential_user.password , user.get("password")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Wrong password")

    tokens = Oauth2.create_access_token(data={"user_id" : str(user.get("_id"))})
    
    return {"access_token" : tokens , "token_type" : "bearer"}
    