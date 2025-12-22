import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ChatJoinRequestHandler,
    CommandHandler,
    ContextTypes,
)

# ===============================
# 🔑 BOT TOKEN (YAHAN DALO)
# ===============================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
# Railway → Variables में BOT_TOKEN डालना है

# ===============================
# 📩 START COMMAND (WELCOME)
# ===============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 *Welcome to Auto Joint Request*\n\n"
        "🎯 *Free & Open Collections*\n"
        "🔗 Use only official links below\n\n"
        "1️⃣ *Open Collection*\n"
        "https://t.me/+cV6_p6hE_Lw2MTE0\n\n"
        "2️⃣ *Instagram Viral Collection*\n"
        "https://t.me/+GLRGYAGH9bc0MTU0\n\n"
        "3️⃣ *Open Hub*\n"
        "https://t.me/+Xc9JoxboVFdmZGJk\n"
    )

    await update.message.reply_text(
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

    # DM small welcome + START button
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
        pass  # user ne bot start nahi kiya ho to ignore

# ===============================
# ▶️ BUTTON CALLBACK
# ===============================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await start(query, context)

# ===============================
# 🚀 MAIN
# ===============================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(ChatJoinRequestHandler(approve_request))
    app.add_handler(
        telegram.ext.CallbackQueryHandler(button_handler)
    )

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
