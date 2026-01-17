from pyrogram import Client
from pymongo import MongoClient, UpdateOne
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

MONGO_URI = "mongodb+srv://Omnibot:Omni123@cluster0.ksvp6ly.mongodb.net/?appName=Cluster0"  # Mongo URI-ni buraya əlavə et
mongo_client = MongoClient(MONGO_URI)

# Database və collection-lar
db = mongo_client["omnibot"]
daily_col = db["daily_messages"]       # Günlük mesajlar
monthly_col = db["monthly_stats"]      # Aylıq toplar
groups_col = db["groups"]              # Botun işlədiyi qruplar

# -------------------------
# 1️⃣ Mesajları qeyd et
# -------------------------
async def record_message(message: Client, client: Client):
    if message.chat.type not in ["group", "supergroup"]:
        return

    # Qrup MongoDB-də yoxdursa əlavə et
    groups_col.update_one(
        {"chat_id": message.chat.id},
        {"$set": {"chat_id": message.chat.id}},
        upsert=True
    )

    data = {
        "chat_id": message.chat.id,
        "user_id": message.from_user.id,
        "username": message.from_user.username,
        "first_name": message.from_user.first_name,
        "text": message.text,
        "date": datetime.utcnow().strftime("%Y-%m-%d")
    }

    daily_col.insert_one(data)

# -------------------------
# 2️⃣ Günlük top 5 istifadəçi
# -------------------------
async def top_users_message(client: Client, chat_id: int):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    pipeline = [
        {"$match": {"chat_id": chat_id, "date": today}},
        {"$group": {"_id": "$user_id", "count": {"$sum": 1}, "first_name": {"$first": "$first_name"}}},
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ]
    results = daily_col.aggregate(pipeline)
    text = f"🌟 Bugünün top 5 istifadəçisi:\n"
    for i, user in enumerate(results, 1):
        text += f"{i}. {user['first_name']} → {user['count']} mesaj\n"

    if text:
        await client.send_message(chat_id, text)

# -------------------------
# 3️⃣ Günlük top 5 komutu
# -------------------------
async def top_users_command(client: Client, message):
    await top_users_message(client, message.chat.id)

# -------------------------
# 4️⃣ Aylıq top istifadəçi
# -------------------------
async def top_month(client: Client, message):
    pipeline = [
        {"$match": {"chat_id": message.chat.id}},
        {"$group": {"_id": "$user_id", "count": {"$sum": 1}, "first_name": {"$first": "$first_name"}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    results = monthly_col.aggregate(pipeline)
    text = "🌟 Aylıq top istifadəçilər:\n"
    for i, user in enumerate(results, 1):
        text += f"{i}. {user['first_name']} → {user['count']} mesaj\n"

    await message.reply_text(text)

# -------------------------
# 5️⃣ Günlük sıfırlama və aylığa əlavə
# -------------------------
async def daily_reset_job(client: Client):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    groups = groups_col.find()
    for group in groups:
        chat_id = group["chat_id"]

        # 1️⃣ Günlük top 5-i paylaş
        await top_users_message(client, chat_id)

        # 2️⃣ Günlük məlumatları aylığa əlavə et
        pipeline = [
            {"$match": {"chat_id": chat_id, "date": today}},
            {"$group": {"_id": "$user_id", "count": {"$sum": 1}, "first_name": {"$first": "$first_name"}}}
        ]
        results = daily_col.aggregate(pipeline)
        ops = []
        for user in results:
            ops.append(UpdateOne(
                {"chat_id": chat_id, "user_id": user["_id"]},
                {"$inc": {"count": user["count"]}, "$set": {"first_name": user["first_name"]}},
                upsert=True
            ))
        if ops:
            monthly_col.bulk_write(ops)

        # 3️⃣ Günlük məlumatları sil
        daily_col.delete_many({"chat_id": chat_id, "date": today})

# -------------------------
# 6️⃣ Scheduler (00:00 Bakı saatı)
# -------------------------
def schedule_daily_reset(client: Client):
    scheduler = AsyncIOScheduler(timezone="Asia/Baku")
    scheduler.add_job(lambda: client.loop.create_task(daily_reset_job(client)), 'cron', hour=0, minute=0)
    scheduler.start()
