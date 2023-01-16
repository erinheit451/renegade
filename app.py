import os
from telegram.ext import Updater, CommandHandler

bot_token = os.environ["BOT_TOKEN"]
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    update.message.reply_text("Hi!")

start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

updater.start_polling()

