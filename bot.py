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

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# ===============================
# START COMMAND
# ===============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 *Welcome to Auto Join Request*\n\n"
        "1️⃣ *Open Collection*\n"
        "https://t.me/+cV6_p6hE_Lw2MTE0\n\n"
        "2️⃣ *Instagram Viral Collection*\n"
        "https://t.me/+GLRGYAGH9bc0MTU0\n\n"
        "3️⃣ *Open Hub*\n"
        "https://t.me/+Xc9JoxboVFdmZGJk\n"
    )

    if update.message:
        await update.message.reply_text(text, parse_mode="Markdown")
    else:
        await update.callback_query.message.reply_text(text, parse_mode="Markdown")

# ===============================
# AUTO APPROVE JOIN REQUEST
# ===============================
async def approve_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.chat_join_request.chat.id
    user_id = update.chat_join_request.from_user.id

    await context.bot.approve_chat_join_request(chat_id, user_id)

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("▶️ START", callback_data="start")]]
    )

    try:
        await context.bot.send_message(
            user_id,
            "✅ *Approved successfully!*\n\nTap START below 👇",
            reply_markup=keyboard,
            parse_mode="Markdown",
        )
    except:
        pass

# ===============================
# BUTTON HANDLER
# ===============================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await start(update, context)

# ===============================
# MAIN
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
