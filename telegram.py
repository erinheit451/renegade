import os
<<<<<<< Updated upstream
import openai
import requests

# Load secure info from .env file
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set up OpenAI API client
openai.api_key = OPENAI_API_KEY

# Initialize chatlog
chatlog = {}

def handle_incoming_message(chat_id, sender, body):
  global chatlog

  # Add the incoming message to the chatlog
  if chat_id not in chatlog:
    chatlog[chat_id] = []
  chatlog[chat_id].append({"sender": sender, "body": body})

  # Calculate the maximum size of the chatlog in tokens
  prompt_size = len(openai.Completion.create(model="text-davinci-003", prompt="").text)
  max_size = 4096 - prompt_size  # Maximum size of the chatlog in tokens

  # Prune the chatlog to remove older messages if needed
  chatlog_size = sum(len(message["body"]) for message in chatlog[chat_id]) 
  while chatlog_size > max_size:
    chatlog_size -= len(chatlog[chat_id].pop(0)["body"])

  # Use the OpenAI API to generate a response to the incoming message
  prompt = "\n".join(f"{message['sender']}: {message['body']}" for message in chatlog[chat_id])
  response = openai.Completion.create( model="text-davinci-003", prompt=prompt, temperature=0.7, max_tokens=4096, top_p=1, frequency_penalty=0, presence_penalty=0 )

  # Send the response back to the sender through the Telegram API
  requests.post( f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", json={ "chat_id": chat_id, "text": response.text } )

def process_update(update):
  if "message" in update:
    # Extract the sender and body of the incoming message
    message = update["message"]
    sender = message["from"]["first_name"]
    body = message["text"]
    # Extract the chat_id of the incoming message
    if "chat" in message:
      chat_id = message["chat"]["id"]
    elif "from" in message:
      chat_id = message["from"]["id"]
    else:
      chat_id = None

    # Call the handle_incoming_message function to process the message
    if chat_id and body:
      handle_incoming_message(chat_id, sender, body)

# Set up a webhook endpoint to listen for updates from the Telegram API
@app.route("/telegram", methods=["POST"])
def telegram_webhook():
  # Extract the update from the request
  update = request.get_json()

  # Process the update
  process_update(update)

Return ok

# Set up the webhook with the Telegram API
requests.post( f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook", json={ "url": f"https://your-app-url.com/telegram" } )

# Send a message to the chat
chat_id = 12345
sender = "Alice"
body = "Hello, this is a test message."
handle_incoming_message(chat_id, sender, body)
=======
from telegram.ext import Updater, CommandHandler

# Import the generate_response function from response.py
from response import generate_response

def telegram_bot():
    # Get the Telegram API key
    telegram_api_key = os.getenv("TELEGRAM_API_KEY")

    # Create the Updater and pass it the API key
    updater = Updater(telegram_api_key, use_context=True)

    # Add a command handler for the /start command
    updater.dispatcher.add_handler(CommandHandler("start", start))

    # Start the bot
    updater.start_polling()
    updater.idle()

def start(update, context):
    # Send a message to the user
    update.message.reply_text("Hello! I am a chatbot. What can I help you with today?")
>>>>>>> Stashed changes
