import os
import openai
import json
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from prompt import prompt

openai.api_key = os.getenv("OPENAI_API_KEY")

# Load conversation log from file
try:
    with open("conversation_log.json", "r") as log_file:
        conversation_log = [entry['user'] for entry in json.load(log_file) if 'user' in entry]
except:
    conversation_log = []

def prune_conversation_log(log, max_tokens=300):
    while len(log) > max_tokens:
        log.pop(0)
    return log

def generate_chatbot_response(prompt, user_input, chatlog):
    chatlog = [message['chatbot'] for message in chatlog]
    chatlog.append(user_input)
    history = "\n".join(chatlog)
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{prompt}\n{history}",
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6
    )
    chatbot_response = response.choices[0].text
    return chatbot_response

# Create the bot
bot = telegram.Bot(token="5751626277:AAG21V-LeR1tNHVjl6bIbDekKVWIVXqyNFA")

# Create the Updater and pass it the bot's token
updater = Updater(bot=bot)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

def handle_message(update: Updater, context: CallbackContext):
    # Get the message from the update
    message = update.message
    # Get the chat ID and message text
    chat_id = message.chat.id
    text = message.text
    # Prune the conversation log
    pruned_log = prune_conversation_log(conversation_log)
    # Generate a response from the chatbot
    chatbot_response = generate_chatbot_response(prompt, text, pruned_log)
    # Send the response to the user
    context.bot.send_message(chat_id=chat_id, text=chatbot_response)
    # Append the response to the conversation log
    conversation_log.append({"chatbot": chatbot_response})
    # Save the updated conversation log to file
    with open("conversation_log.json", "w") as log_file:
      json.dump(conversation_log, log_file)

 # Add a handler to the dispatcher to handle messages
    dispatcher.add_handler(MessageHandler(callback=handle_message))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

def start_bot():
    updater.start_polling()
    updater.idle()





