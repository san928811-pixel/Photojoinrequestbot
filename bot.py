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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 Welcome\n\n"
        "1️⃣ Open Collection\n"
        "https://t.me/+cV6_p6hE_Lw2MTE0\n\n"
        "2️⃣ Instagram Viral\n"
        "https://t.me/+GLRGYAGH9bc0MTU0\n\n"
        "3️⃣ Open Hub\n"
        "https://t.me/+Xc9JoxboVFdmZGJk\n"
    )

    if update.message:
        await update.message.reply_text(text)
    else:
        await update.callback_query.message.reply_text(text)

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.chat_join_request.chat.id
    user = update.chat_join_request.from_user.id
    await context.bot.approve_chat_join_request(chat, user)

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("▶️ START", callback_data="start")]]
    )

    try:
        await context.bot.send_message(
            user,
            "✅ Approved!\nTap START 👇",
            reply_markup=keyboard
        )
    except:
        pass

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await start(update, context)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(ChatJoinRequestHandler(approve))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()
