from pyrogram import Client
from pyrogram.types import Message

async def show_id(message: Message, client: Client):
    """
    İstifadəçiyə öz Telegram ID-sini göstərir
    """
    user = message.from_user
    if user:
        text = f"Salam, {user.first_name}!\nSənin Telegram ID-n: `{user.id}`"
        await message.reply_text(text, parse_mode="Markdown")
    else:
        await message.reply_text("ID-ni əldə edə bilmədim.")
