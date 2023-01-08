import os
import openai
import telegram_bot
import requests
from flask import Flask, request, Response, redirect, render_template, url_for
from prompt import prompt
from response import generate_chatbot_response
from chatlog import log_conversation, load_conversation_log, prune_conversation_log
from record import log_permanent_record, load_permanent_record

openai.api_key = os.getenv("OPENAI_API_KEY")
api_token = os.getenv('TELEGRAM_API_TOKEN')

bot = telegram_bot.Bot(token=api_token)

app = Flask(__name__)

conversation = []
conversation = load_conversation_log()
log_conversation(conversation)

def set_webhook():
    url = "https://api.telegram.org/bot{}/setWebhook".format(api_token)
    # Set the webhook to the URL of your Flask app
    response = requests.post(url, data={'url': 'https://renegade.herokuapp.com/hook'})
    print(response.status_code)


@app.route('/hook', methods=['POST'])
def webhook_handler():
    # Get the update from Telegram
    update = telegram_bot.Update.de_json(request.get_json(force=True), bot)
    # Update the conversation log
    conversation.append({"user": update.message.text})
    # Generate a response
    chatlog = prune_conversation_log(conversation)
    chatbot_response = generate_chatbot_response(prompt, update.message.text, chatlog)
    conversation.append({"chatbot": chatbot_response})
    log_permanent_record(conversation)
    # Send the response to Telegram
    bot.send_message(chat_id=update.message.chat_id, text=chatbot_response)
    return 'ok'

