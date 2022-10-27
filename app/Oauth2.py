from jose import JWTError , jwt
from datetime import datetime , timedelta
from fastapi import HTTPException , Depends , status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from . import schema
from . import database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data:dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})

    encode_jwt = jwt.encode(to_encode, SECRET_KEY , algorithm=ALGORITHM)

    return encode_jwt

def verify_access_token(token:str , credential_exception):

        try:
            payload = jwt.decode(token, SECRET_KEY , algorithms=ALGORITHM)
            id = payload.get("user_id")

            if not id:
                raise credential_exception
            token_data = schema.tokenData(id=id)
        except JWTError:
            raise credential_exception
        return token_data

async def get_current_user(tokens:str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"})

    decode_token = verify_access_token(token=tokens, credential_exception=credential_exception)
    
    user = await database.get_user_by_id(decode_token.id)
    return user 