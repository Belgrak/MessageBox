import logging
import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message as AiogramMessage, BotCommand
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis
from pydantic import BaseModel

# Get Telegram bot token from environment variable
API_TOKEN = os.getenv('TELEGRAM_BOT_API_TOKEN')

if API_TOKEN is None:
    raise ValueError("The environment variable 'TELEGRAM_BOT_API_TOKEN' is not set")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Database configuration
MONGO_DETAILS = "mongodb://mongo:27017"
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.messages
message_collection = database.get_collection("messages")

# Redis configuration
redis = Redis(host='redis', port=6379, db=0)


class Message(BaseModel):
    author: str
    content: str


async def fetch_messages():
    messages = []
    async for message in message_collection.find():
        messages.append(Message(**message))
    return messages


async def setup_bot_commands():
    bot_commands = [
        BotCommand(command="/help", description="Get info about me"),
        BotCommand(command="/messages", description="Get all messages"),
    ]
    await bot.set_my_commands(bot_commands)


@dp.message(Command(commands=["start", "help"]))
async def send_welcome(message: AiogramMessage):
    await setup_bot_commands()
    await message.answer("Hi!\nI'm your bot!\nUse /messages to get all messages or send message to add another one.")


@dp.message(Command(commands=["messages"]))
async def get_messages(message: AiogramMessage):
    cached_messages = await redis.get("messages")
    if cached_messages:
        await message.answer(cached_messages.decode('utf-8'))
    else:
        messages = await fetch_messages()
        messages_text = "\n".join([f"{msg.author}: {msg.content}" for msg in messages])
        if len(messages) == 0:
            messages_text = "No messages"
        await redis.set("messages", messages_text)
        await message.answer(messages_text)


@dp.message()
async def create_message(message: AiogramMessage):
    author = message.from_user.username
    new_msg = Message(author=author, content=message.text)
    await message_collection.insert_one(new_msg.dict())
    await redis.flushall()  # Clear the cache
    await message.answer(f"Message from {author} added!")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
