import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    ChatJoinRequestHandler,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ===============================
# 🔑 BOT TOKEN (ENV VARIABLE)
# ===============================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

# ===============================
# 📩 START COMMAND (WELCOME)
# ===============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 *Welcome to Auto Join Request*\n\n"
        "🎯 *Free & Open Collections*\n"
        "🔗 Use only official links below\n\n"
        "1️⃣ *Open Collection*\n"
        "https://t.me/+cV6_p6hE_Lw2MTE0\n\n"
        "2️⃣ *Instagram Viral Collection*\n"
        "https://t.me/+GLRGYAGH9bc0MTU0\n\n"
        "3️⃣ *Open Hub*\n"
        "https://t.me/+Xc9JoxboVFdmZGJk\n"
    )

    if update.message:
        await update.message.reply_text(
            welcome_text,
            parse_mode="Markdown"
        )
    elif update.callback_query:
        await update.callback_query.message.reply_text(
            welcome_text,
            parse_mode="Markdown"
        )

# ===============================
# ✅ AUTO JOIN REQUEST HANDLER
# ===============================
async def approve_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.chat_join_request.chat.id
    user_id = update.chat_join_request.from_user.id

    # Approve join request
    await context.bot.approve_chat_join_request(chat_id, user_id)

    # DM welcome + START button
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("▶️ START", callback_data="start")]]
    )

    try:
        await context.bot.send_message(
            chat_id=user_id,
            text="✅ *You are approved!*\n\n👇 Tap below to get welcome & links",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    except:
        # User ne bot start nahi kiya ho to Telegram DM allow nahi karta
        pass

# ===============================
# ▶️ BUTTON CALLBACK
# ===============================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await start(update, context)

# ===============================
# 🚀 MAIN
# ===============================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(ChatJoinRequestHandler(approve_request))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
