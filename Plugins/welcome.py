from pyrogram import Client, filters
from pyrogram.types import Message
from pymongo import MongoClient
from datetime import datetime, timedelta
import asyncio

MONGO_URI = "mongodb+srv://Omnibot:Omni123@cluster0.ksvp6ly.mongodb.net/?appName=Cluster0"
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["omnibot"]
groups_col = db["groups"]           # Botun işlədiyi qruplar
welcome_col = db["welcome_messages"] # Salam mesajları və vaxtları

# Yeni istifadəçi gəldikdə salamla
async def welcome_new_member(client: Client, message: Message):
    chat_id = message.chat.id

    for member in message.new_chat_members:
        # Salam mesajı
        text = f"Salam, {member.mention}! 👋\nXoş gəlmisən {message.chat.title} qrupuna!"
        sent_msg = await message.reply_text(text)

        # MongoDB-də saxla: mesaj_id və silinmə vaxtı
        delete_time = datetime.utcnow() + timedelta(hours=1)
        welcome_col.insert_one({
            "chat_id": chat_id,
            "message_id": sent_msg.message_id,
            "delete_time": delete_time
        })

# 1 saat sonra salam mesajını silən funksiya
async def delete_expired_welcome(client: Client):
    now = datetime.utcnow()
    expired = welcome_col.find({"delete_time": {"$lte": now}})
    for msg in expired:
        try:
            await client.delete_messages(msg["chat_id"], msg["message_id"])
        except:
            pass
        welcome_col.delete_one({"_id": msg["_id"]})

# Scheduler: hər 5 dəqiqədən bir expired mesajları sil
def schedule_welcome_cleanup(client: Client):
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    scheduler = AsyncIOScheduler(timezone="Asia/Baku")
    scheduler.add_job(lambda: client.loop.create_task(delete_expired_welcome(client)), 'interval', minutes=5)
    scheduler.start()
