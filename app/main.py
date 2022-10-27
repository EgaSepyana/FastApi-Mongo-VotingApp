from fastapi import FastAPI
from .router import candidate , user , auth , vote
app = FastAPI()

app.include_router(candidate.router)
app.include_router(user.router)
app.include_router(vote.router)
app.include_router(auth.router)

@app.get('/')
async def root():
    return {"Massage" : "test"}

