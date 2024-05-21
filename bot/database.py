from aioredis import Redis
from os import environ
from bot.config import Database

REDIS_URI = Database.REDIS_URI.split(":")
db = Redis(
    host=REDIS_URI[0],
    port=REDIS_URI[1],
    password=Database.REDIS_PASSWORD,
    decode_responses=True,
)

def s_l(text):
    return text.split(" ")

def l_s(list):  # Returns String
    str = " ".join(f"{x}" for x in list)
    return str.strip()

async def is_inserted(var, id):
    try:
        users = await fetch_all(var)
        return str(id) in users
    except Exception as e:
        return False

async def insert(var, id): 
    try:
        users = await fetch_all(var)
        users.append(id)
        await db.set(var, l_s(users))
        return True
    except Exception as e:
        return False
        print(e)
        
async def fetch_all(var): 
    users = await db.get(var)
    return [""] if users is None or users == "" else s_l(users)
    
async def delete(var, id):
    try:
        users = await fetch_all(var)
        users.remove(id)
        await db.set(var, l_s(users))
        return True
    except Exception as e:
        print(e)
        return False
