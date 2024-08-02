import os
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from redis.asyncio import Redis
from fastapi_pagination import Page, paginate, add_pagination
from fastapi_pagination.utils import disable_installed_extensions_check

app = FastAPI()

# Database configuration
MONGO_DETAILS = "mongodb://mongo:27017"
client = AsyncIOMotorClient(MONGO_DETAILS)
app.mongodb_client = client
database = client.get_database("messages")
message_collection = database.get_collection("messages")

# Redis configuration
redis = Redis(host='redis', port=6379, db=0)


# Message model
class Message(BaseModel):
    author: str
    content: str


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


@app.get("/api/v1/messages/", response_model=Page[Message])
async def get_messages():
    messages = []
    async for message in message_collection.find():
        messages.append(Message(**message))
    disable_installed_extensions_check()
    return paginate(messages)


@app.post("/api/v1/message/")
async def create_message(message: Message):
    message_dict = message.dict()
    await message_collection.insert_one(message_dict)
    await redis.flushall()  # Clear the cache
    return message


add_pagination(app)
