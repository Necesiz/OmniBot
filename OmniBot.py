from pyrogram import Client, filters
from Plugins import start, help, tag, user_id, stats, welcome, active_users, filter, questions, broadcast

app = Client("OmniBotSession", 
api_id=YOUR_API_ID,
api_hash="YOUR_API_HASH", 
bot_token="YOUR_BOT_TOKEN")

# Start komutu
@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    await start.start_message(message, client)

# Help komutu
@app.on_message(filters.command("help"))
async def help_cmd(client, message):
    await help.help_message(message, client)

# Digər pluginləri əlavə et
@app.on_message(filters.command(["tag", "tag5"]))
async def tag_cmd(client, message):
    await tag.tag_users(message, client)

@app.on_message(filters.command("id"))
async def id_cmd(client, message):
    await user_id.show_id(message, client)

@app.on_message(filters.text)
async def echo_cmd(client, message):
    await stats.record_message(message, client)  # günlük stats
    await filter.check_message(message, client)  # söyüş filteri

# Qrup aktivliyi üçün periodic suallar
questions.schedule_questions(app)

app.run()
