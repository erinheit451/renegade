import os
from telegram.ext import Updater, CommandHandler

bot_token = os.environ["BOT_TOKEN"]
bot = telegram.Bot(token=bot_token)
updater = Updater(bot=bot, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    update.message.reply_text("Hi!")

start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

updater.start_polling()

