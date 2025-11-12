from pyrogram import Client, filters

# === তোমার তথ্য ===
API_ID = 30333773  # তোমার api_id
API_HASH = "2a5bd1372c4d05bc2800a962b69d7d4d"
BOT_TOKEN = "8515802854:AAHpL-Dhkf3btfeH6zTXwAVVSWN4pUL67W8"
ADMIN_ID = 5098702978  # এখানে তোমার Telegram numeric ID বসাও
# ===================

app = Client("file_request_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text("👋 হ্যালো! আমি ফাইল শেয়ার বট 🤖\n\nতুমি চাইলে `/request ফাইলের_নাম` লিখে ফাইল রিকোয়েস্ট করতে পারো।")

# --- ইউজার রিকোয়েস্ট করলে ---
@app.on_message(filters.command("request"))
def request_file(client, message):
    if len(message.command) < 2:
        message.reply_text("⚠️ ব্যবহার: `/request ফাইলের_নাম`\n\nউদাহরণ: `/request Physics Book`", quote=True)
        return

    req_text = " ".join(message.command[1:])
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    # ইউজারকে রেসপন্স
    message.reply_text("✅ তোমার রিকোয়েস্ট অ্যাডমিনের কাছে পাঠানো হয়েছে। কিছুক্ষণ অপেক্ষা করো।")

    # অ্যাডমিনকে ফরওয়ার্ড
    client.send_message(
        ADMIN_ID,
        f"📩 নতুন ফাইল রিকোয়েস্ট এসেছে:\n\n👤 ইউজার: {user_name}\n🆔 ID: `{user_id}`\n📦 রিকোয়েস্ট: {req_text}\n\nউত্তর দিতে লিখো:\n`/send {user_id}` তারপর ফাইল পাঠাও।"
    )

# --- অ্যাডমিন ফাইল পাঠালে ---
@app.on_message(filters.command("send") & filters.user(ADMIN_ID))
def send_to_user(client, message):
    if len(message.command) < 2:
        message.reply_text("⚠️ ব্যবহার: `/send user_id`\n\nতারপর ফাইল পাঠাও।")
        return

    global target_user
    target_user = int(message.command[1])
    message.reply_text(f"📤 এখন যে ফাইল পাঠাবে, সেটা {target_user} আইডির ইউজারকে পাঠানো হবে।")

# --- অ্যাডমিন ফাইল পাঠালে তা ইউজারকে পাঠানো হবে ---
@app.on_message(filters.user(ADMIN_ID) & (filters.document | filters.video | filters.photo | filters.audio))
def forward_file(client, message):
    try:
        client.copy_message(target_user, ADMIN_ID, message.id)
        message.reply_text("✅ ফাইল ইউজারের কাছে পাঠানো হয়েছে।")
    except Exception as e:
        message.reply_text(f"⚠️ ত্রুটি: {e}")

app.run()