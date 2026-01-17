from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asyncio import sleep

async def start_message(message, client):
    buttons = [
        [InlineKeyboardButton("Əmrlər", callback_data="commands")],
        [InlineKeyboardButton("Sahib", url="https://t.me/SAHIB_USERNAME")]
    ]
    sent = await message.reply_text(
        "Salam! Mən OmniBot, qrupun idarəçisi və çoxfunksiyalı köməkçin! 🤖",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    await sleep(3600)  # 1 saat
    await sent.delete()
    await message.delete()
