import os
import telegram
import openai
import logging
import time
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from flask import Flask, request
from gunicorn.app.base import Application

load_dotenv()

app = Flask(__name__)

# Set the OpenAI API key
openai.api_key = os.environ['openai_api_key']
bot_token = os.environ['bot_token']

# Create the Telegram bot
bot = telegram.Bot(token=bot_token)

# Define the /start command handler
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I am a bot that is integrated with the OpenAI GPT-3 API. You can ask me any question and I will try to provide a response.")

# Define the /help command handler
def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="To use me, simply send me a message with your question. I will use the OpenAI GPT-3 API to generate a response based on the information I have been trained on.")

# Define the message handler
def message(update, context):
    # Get the message text
    message_text = update.message.text

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=message_text,
        max_tokens=250,
        temperature=0.7
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=response["choices"][0]["text"])

# Setting the command and message handlers
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(MessageHandler(Filters.text, message))

def error(update, context):
    logger = logging.getLogger(__name__)
    # Log the error
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    # Register the error handler
    dispatcher.add_error_handler(error)

# Start the polling
updater.start_polling()

# Wait for some time before sending the "hi" message
time.sleep(5)

# Send a "hi" message to the chat of the last user who interacted with the bot
last_chat_id = bot.getUpdates()[-1].message.chat_id
bot.send_message(chat_id=last_chat_id, text="hi")

# Create a route for the webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    # Get the update from Telegram
    update = request.get_json()

    # Pass the update to the Telegram bot
    updater.dispatcher.process_update(update)

    # Return a 200 OK response
    return 'OK'

# Set the webhook
try:
    bot.setWebhook(url='https://coaster-amusement-mile.herokuapp.com/webhook')
    print("Webhook set successfully.")
except telegram.TelegramError as e:
    print(f"Webhook set failed: {e}")

if __name__ == '__main__':
    app.run()