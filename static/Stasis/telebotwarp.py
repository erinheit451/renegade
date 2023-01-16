import os
import openai
import telegram
import logging
from flask import Flask, request
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters
from telegram import Update

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
bot_token = os.environ["BOT_TOKEN"]
bot = telegram.Bot(token=bot_token)

def handle_text(update: Update, context: CallbackContext):
    message_text = update.message.text
    chat_id = update.message.chat.id
    response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=message_text,
            max_tokens=250,
            temperature=0.7
    )
    bot.send_message(chat_id=chat_id, text=response["choices"][0]["text"])

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()
    context = CallbackContext()
    if 'message' in update:
        handle_text(update, context)
    return "OK"

updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.text, handle_text))

def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    context.bot.send_message(chat_id=chat_id, text="Hi!")
dispatcher.add_handler(CommandHandler("start", start))

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

updater.start_polling()

if __name__ == '__main__':
    app.run()