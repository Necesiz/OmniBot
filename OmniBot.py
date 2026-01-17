from pyrogram import Client, filters
from Plugins import start, help, tag, user_id, stats, welcome, active_users, questions, broadcast
from Plugins import stats
from pyrogram import Client, filters
from Plugins import welcome
from pyrogram import filters

app = Client("OmniBotSession", 
api_id=23860620,
api_hash="347c94d92d0bbcfbc223651b73d71345", 
bot_token="8533476973:AAGtXR0dLk4jByOzPRjf6A8JB04tJA3UCRY")

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

@app.on_message(filters.command("id"))
async def id_cmd(client, message):
    await user_id.show_id(message, client)

# Hər mesaj üçün qeyd
@app.on_message(filters.text)
async def handle_text(client, message):
    await stats.record_message(message, client)

# Günlük top 5 komutu
@app.on_message(filters.command("top"))
async def top_cmd(client, message):
    await stats.top_users_command(client, message)

# Aylıq top komutu
@app.on_message(filters.command("top_month"))
async def top_month_cmd(client, message):
    await stats.top_month(client, message)

# Yeni üzv gəldikdə salamla
@app.on_message(filters.new_chat_members)
async def new_member(client, message):
    await welcome.welcome_new_member(client, message)

# Qrup aktivliyi üçün periodic suallar
questions.schedule_questions(app)

app.run()
