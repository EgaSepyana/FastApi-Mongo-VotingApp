from fastapi import APIRouter , HTTPException , status , Response , Depends
from .. import database
from .. import schema
from ..  import Oauth2

router = APIRouter(
    prefix="/post",
    tags=["postcandidate"]
)

@router.post('/', response_model=schema.postOut)
async def input_candidate(posts:schema.post , Current_user:dict = Depends(Oauth2.get_current_user)):
    role = Current_user.get("role")

    if role == "user":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Oly Admin And Super Admin Can Add Candicate")

    data = await database.add_candidate(posts.dict())
    data["_id"] = str(data.get("_id"))
    return data

@router.get("/{id}")
async def get_data_by_id(id:str, Current_user:dict = Depends(Oauth2.get_current_user)):
    data = await database.get_data_by_id(id)
    data["_id"] = str(data.get("_id"))
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data Has not Found")
    return data

@router.get("/")
async def get_all_candidate(Current_user:dict = Depends(Oauth2.get_current_user)):
    is_active = Current_user.get("is_active")
    if not is_active:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE , detail="Your Has Disable for this request")
    return await database.get_all_candidate()

@router.delete("/{id}")
async def delete_by_id(id:str, Current_user:dict = Depends(Oauth2.get_current_user)):
    role = Current_user.get("role")

    if role == "user":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Oly Admin And Super Admin Can Delete Candicate")
    
    data = await database.delete_candidate(id)

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You Try To Delete None Data")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schema.postOut)
async def update_candidate_via_id(id:str, payload:schema.updatedPost , Current_user:dict = Depends(Oauth2.get_current_user)):
    role = Current_user.get("role")

    if role == "user":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Oly Admin And Super Admin Can Update Candicate")
    
    old_post = await database.get_data_by_id(id)

    if not old_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Your Data Not Found")
    data = {
        "nama" : old_post.get('nama') if not payload.nama else payload.nama,
        "jurusan" : old_post.get('jurusan') if not payload.jurusan else payload.jurusan,
        "kelas" : old_post.get('kelas') if not payload.kelas else payload.kelas,
        "sekolah" : old_post.get('sekolah') if not payload.sekolah else payload.sekolah,
        "motto" : old_post.get('motto') if not payload.motto else payload.motto
    }

    return await database.update_candidate(data,id)