import os
import telegram
from telegram.ext import Updater, MessageHandler, Filters

# Create the bot
bot = telegram.Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])

# Create the Updater
updater = Updater(bot=bot)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# Define a handler for messages
def handle_message(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    context.bot.send_message(chat_id=chat_id, text=f"You said: {text}")

# Add the handler to the dispatcher
dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

# Start the bot
updater.start_polling()
