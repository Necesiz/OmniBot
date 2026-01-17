from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio

async def tag_users(message: Message, client: Client):
    """
    Bütün istifadəçiləri tag etmək üçün /tag komutu
    /tag5 komutu → 5-lik tag
    """
    chat = message.chat
    text = message.text.lower()

    members = []
    async for member in client.get_chat_members(chat.id):
        # Bot və adminləri istisna edə bilərik əgər istəyirsənsə
        members.append(member.user.mention)

    if "tag5" in text:
        # 5-lik qruplar
        chunk_size = 5
    else:
        # hamısını tag et
        chunk_size = len(members)

    # Mesajları qruplara bölək
    for i in range(0, len(members), chunk_size):
        chunk = members[i:i+chunk_size]
        msg = " ".join(chunk)
        try:
            await message.reply_text(msg)
            await asyncio.sleep(1)  # Flood riskini azaltmaq üçün kiçik gecikmə
        except Exception as e:
            print(f"Tag error: {e}")
