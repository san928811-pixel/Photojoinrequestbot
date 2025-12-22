import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ChatJoinRequestHandler,
    ContextTypes,
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# =========================
# CHANNEL LIST (EDIT HERE)
# =========================
CHANNELS = [
    ("🔥 Open Collection", "https://t.me/+cV6_p6hE_Lw2MTE0"),
    ("📸 Instagram Viral", "https://t.me/+GLRGYAGH9bc0MTU0"),
    ("💎 Open Hub", "https://t.me/+Xc9JoxboVFdmZGJk"),
]

# =========================
# /start → ONLY START BUTTON
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("▶️ START", callback_data="show_links")]]
    )

    await update.effective_message.reply_text(
        "👋 *Welcome!*\n\n"
        "🎁 START दबाओ – आपको gift / links मिलेंगे 👇",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

# =========================
# START BUTTON → SHOW CHANNELS
# =========================
async def show_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(name, url=link)]
        for name, link in CHANNELS
    ]

    await query.message.reply_text(
        "✅ *Welcome 🎉*\n\n"
        "👇 नीचे हमारे official channels हैं:\n"
        "Join करके पूरा access पाएं",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# =========================
# AUTO JOIN REQUEST APPROVE
# + DM WELCOME WITH START
# =========================
async def approve_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # approve join request
        await context.bot.approve_chat_join_request(
            update.chat_join_request.chat.id,
            update.chat_join_request.from_user.id
        )

        # send DM welcome + START button
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("▶️ START", callback_data="show_links")]]
        )

        await context.bot.send_message(
            chat_id=update.chat_join_request.from_user.id,
            text=(
                "🎉 *Welcome!*\n\n"
                "🎁 START दबाओ, आपको gift / official links मिलेंगे 👇"
            ),
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

    except:
        # rate-limit / user ne bot start nahi kiya
        pass

# =========================
# MAIN
# =========================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(show_links, pattern="show_links"))
    app.add_handler(ChatJoinRequestHandler(approve_request))

    print("🤖 Bot running (Public + High Traffic Safe)")
    app.run_polling()

if __name__ == "__main__":
    main()
