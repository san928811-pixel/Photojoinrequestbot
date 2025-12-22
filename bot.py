import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ChatJoinRequestHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 *Welcome to Auto Join Request Bot*\n\n"
        "🔗 *Collections*\n\n"
        "1️⃣ Open Collection\n"
        "https://t.me/+cV6_p6hE_Lw2MTE0\n\n"
        "2️⃣ Instagram Viral Collection\n"
        "https://t.me/+GLRGYAGH9bc0MTU0\n\n"
        "3️⃣ Open Hub\n"
        "https://t.me/+Xc9JoxboVFdmZGJk"
    )

    await update.message.reply_text(text, parse_mode="Markdown")


# auto approve join request
async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    req = update.chat_join_request
    await context.bot.approve_chat_join_request(
        chat_id=req.chat.id,
        user_id=req.from_user.id
    )

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("▶️ START", callback_data="start")]]
    )

    try:
        await context.bot.send_message(
            chat_id=req.from_user.id,
            text="✅ Approved!\nTap START below 👇",
            reply_markup=keyboard
        )
    except:
        pass


# button handler
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await start(update.callback_query, context)


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(ChatJoinRequestHandler(approve))
    app.add_handler(CallbackQueryHandler(button))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
