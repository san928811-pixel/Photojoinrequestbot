import os
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    ChatJoinRequestHandler,
    CallbackContext
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

def start(update: Update, context: CallbackContext):
    update.message.reply_text("✅ Bot is running!")

def approve_request(update: Update, context: CallbackContext):
    try:
        update.chat_join_request.approve()
    except Exception as e:
        print(e)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(ChatJoinRequestHandler(approve_request))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
