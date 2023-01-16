import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

bot_token = os.environ["BOT_TOKEN"]
bot = telegram.Bot(token=bot_token)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I am a bot.")

def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I am a simple bot. Send me a message and I will respond.")

def message(update, context):
    message_text = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text="You said: " + message_text)

updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(MessageHandler(Filters.text, message))

if __name__ == '__main__':
    updater.start_polling()
