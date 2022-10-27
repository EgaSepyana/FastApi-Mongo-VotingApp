import pymongo
from bson.objectid import ObjectId
from datetime import datetime , timedelta

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["mydatabase"]

mycol = mydb["candidate"]
user = mydb["user"]
verification_code = mydb["verification_code"]
vote = mydb["vote"]

user.create_index('email', unique=True)
vote.create_index('user_email', unique=True)

async def fetch_all(Cursor):
    data = []
    for i in Cursor:
        i["_id"] = str(i.get("_id"))
        data.append(i)

    return data

async def add_candidate(data:dict):    
    data['created_at'] = datetime.now()
    mycol.insert_one(data)
    return data

async def get_all_candidate():
    all_data = mycol.find().sort("nama")
    return await fetch_all(all_data)

async def get_data_by_id(id):
    try:
        id = ObjectId(id)
        query = {"_id": id}
        data = mycol.find_one(query)
    except:
        return False

    if not data:
        return False

    return data
    

async def update_candidate(data:dict, id:int):
    try:
        id = ObjectId(id)
        query = {"_id" : id}
        new_data = {"$set" : data}
        mycol.update_one(query, new_data)
    except:
        return False
    return mycol.find_one(query)

async def delete_candidate(id:int):
    try:
        id = ObjectId(id)
        query = {"_id" : id}
        old_data = await get_data_by_id(id)
    except:
        return False
    if not old_data:
        return False
        
    mycol.delete_one(query)

    return True

async def create_user(data:dict):
    data['created_at'] = datetime.now()
    user.insert_one(data)
    return data

async def get_all_user():
    all_data = user.find()
    return await fetch_all(all_data)

async def get_user_by_email(email:str):
    query = {"email" : email}
    users = user.find_one(query)
    if not users:
        return False
    return users

async def get_user_by_id(id:str):
    id = ObjectId(id)
    query = {"_id" : id}
    users = user.find_one(query)

    return users

async def disable_user(email:str , data:dict):
    query = {"email" : email}
    new_data = {"$set" : data}
    user.update_one(query, new_data)
    
    return await get_user_by_email(email)

async def get_user_by_email(email:str):
    query = {"email" : email}
    data = user.find_one(query)
    if not data:
        return False
    return data    

async def update_user_password(password:str, email:str):
    user_email = {"email" : email}
    updated_password = {"password" : password}
    query = {"$set" : updated_password}
    user.update_one(user_email, query)

    return True

async def add_verif_code():
    data = {}
    data["expire_code"] = datetime.utcnow() + timedelta(minutes=3)
    verification_code.insert_one(data)
    return data

async def get_verif_code(verif_code:str) -> dict:
    try:
        verif_code = ObjectId(verif_code)
        return verification_code.find_one({"_id" : verif_code})
    except:
        return False

async def vote_candidate(id:str, email:str):
    data = {
        "candidate_id" : id,
        "user_email": email
    }

    vote.insert_one(data)
    return True

async def delete_vote_candidate(email:str):
    query = {"user_email": email}
    vote.delete_one(query)
    return True

async def find_vote_by_email(email:str):
    query = {"user_email" : email}
    return vote.find_one(query)

async def get_all_candidate_by_candicate_id(id:str):
    # query = {"candidate_id" : id}
    # vote_data = vote.
    # return fetch_all()
    pass
# a = []
 
# for i in mycol.find({},{ "_id": 0}):
#     a.append(i)

# print(a)
