from datetime import datetime
from pydantic import BaseModel , EmailStr
from typing import Optional
from pydantic.types import conint

class post(BaseModel):
    nama: str
    jurusan: str
    kelas: int
    sekolah: str
    motto:str

    class Config:
        schema_extra = {
            "example": {
                "nama": "Foo",
                "jurusan": "Kimia Industri",
                "kelas": 11,
                "sekolah": "SMKN 1 Cimahi",
                "motto": "Your motto"
            }
        }

class postOut(post):
    _id :int
    created_at:datetime

    class Config:
        orm_mode = True

class updatedPost(BaseModel):
    nama: Optional[str] = ''
    jurusan: Optional[str] = ''
    kelas: Optional[int] = 0
    sekolah: Optional[str] = ''
    motto: Optional[str] = ''

class Users(BaseModel):
    role:Optional[str] = "user"
    email:EmailStr
    password:str
    is_active: Optional[bool] = True

    class Config:
        schema_extra = {
            "example": {
                "role" : "user",
                "email" : "user@gmail.com",
                "password" : "rahasia",
                "is_active" : True
            }
        }

class userOut(BaseModel):
    email:str
    role:str
    is_active:bool
    
    class Config:
        orm_mode = True

class tokenData(BaseModel):
    id: Optional[str] = None

class Token(BaseModel):
    access_token : str
    token_type: str

class diable_user(BaseModel):
    is_active:bool

    class Config:
        schema_extra = {
            "example": {
                "is_active" : True
            }
        }

class Change_password(BaseModel):
    old_password:str
    new_password:str

class Gmail_user(BaseModel):
    your_active_gmail:EmailStr
    class Config:
        schema_extra = {
            "example": {
                "your_active_gmail" : "youractivegmail@gmail.com"
            }
        }
class verifycation_code(BaseModel):
    verifycation_code: str

class vote_candidate(BaseModel):
    candidate_id:str
    dir:conint(le=1)