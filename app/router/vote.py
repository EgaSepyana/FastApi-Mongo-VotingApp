from fastapi import APIRouter, HTTPException, status , Depends
from .. import schema
from .. import database
from .. import Oauth2

router = APIRouter(
    prefix="/vote",
    tags=["vote"]
)

@router.post("/test")
async def vote_candicate(vote:schema.vote_candidate, Current_user:dict = Depends(Oauth2.get_current_user)):
    verify_user_exist = await database.find_vote_by_email(Current_user.get("email"))
    verify_candidate_exsit = await database.get_data_by_id(vote.candidate_id)
    print(verify_user_exist)
    print(Current_user.get("email"))
    if vote.dir:
        if verify_candidate_exsit:

            if not verify_user_exist:
                data = await database.vote_candidate(email=Current_user.get("email"), id=vote.candidate_id)
                if data:
                    return {"Massage" : "Succsesfull add vote"}
            raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail="You Already Vote A Candidate")
    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="candidate has not exist")
    else:
        if verify_candidate_exsit:
            if verify_user_exist:
                data = await database.delete_vote_candidate(email=Current_user.get("email"))
                if data:
                    return {"Message" : "Successfull deleted Vote"}
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="your not vote candidate")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="candidate has not exist")