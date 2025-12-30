import os
import json
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ChatJoinRequestHandler,
    CommandHandler,
    ContextTypes,
)

# ======================
# CONFIG
# ======================
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# 👇 आपकी ADMIN ID (FIXED)
ADMIN_ID = 7794044707

DATA_FILE = "active_chats.json"

# 🔗 WELCOME LINKS (FINAL – AS YOU GAVE)
CHANNELS = [
    ("1️⃣ Open Hub", "https://t.me/+io6YMU0BtAs0MzZk"),
    ("2️⃣ Open Collection", "https://t.me/+FK2K07SHP8kzZjRk"),
    ("3️⃣ Specia hub", "https://t.me/+b7jlwKJ5wI8xYjM0"),
    ("4️⃣ Instagram Collection", "https://t.me/+dVLzuQk-msw3MjBk"),
]

# ======================
# HELPERS
# ======================
def load_chats():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_chats(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ======================
# /start (simple)
# ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "यह auto join request bot है.\n"
        "Join request approve होने पर details DM में मिल जाएँगी ✅"
    )

# ======================
# AUTO APPROVE + WELCOME DM + TRACK CHAT
# ======================
async def approve_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.chat_join_request.chat
    user = update.chat_join_request.from_user

    # 1️⃣ Approve join request
    await context.bot.approve_chat_join_request(chat.id, user.id)

    # 2️⃣ Save active group/channel
    data = load_chats()
    cid = str(chat.id)
    if cid not in data:
        data[cid] = {
            "title": chat.title,
            "type": chat.type  # group / supergroup / channel
        }
        save_chats(data)

    # 3️⃣ Build welcome + 4 links message
    text = (
        "👋 Welcome!\n\n"
        "आपका join request approve हो गया है ✅\n\n"
        "👇 हमारे official channels:\n\n"
    )

    for name, link in CHANNELS:
        text += f"{name}\n{link}\n\n"

    # 4️⃣ Send DM (safe – only once)
    try:
        await context.bot.send_message(
            chat_id=user.id,
            text=text
        )
    except:
        pass  # user ne bot start nahi kiya ho

# ======================
# ADMIN COMMAND: /count
# ======================
async def count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    data = load_chats()
    total = len(data)

    await update.message.reply_text(
        f"📊 BOT USAGE\n\n"
        f"✅ Total Active Groups/Channels: {total}"
    )

# ======================
# ADMIN COMMAND: /list
# ======================
async def list_chats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    data = load_chats()
    if not data:
        await update.message.reply_text("❌ No active groups/channels found.")
        return

    msg = "📋 ACTIVE GROUPS / CHANNELS\n\n"
    for i, info in enumerate(data.values(), start=1):
        msg += f"{i}. {info['title']} ({info['type']})\n"

    await update.message.reply_text(msg)

# ======================
# MAIN
# ======================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(ChatJoinRequestHandler(approve_request))
    app.add_handler(CommandHandler("count", count))
    app.add_handler(CommandHandler("list", list_chats))

    print("🤖 Bot running (Welcome + 4 Links + Tracking)")
    app.run_polling()

if __name__ == "__main__":
    main()
