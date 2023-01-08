import os
import openai
import telegram
import requests
from flask import Flask, request, Response
from prompt import prompt
from response import generate_chatbot_response
from chatlog import log_conversation, load_conversation_log, prune_conversation_log
from record import log_permanent_record, load_permanent_record

openai.api_key = os.getenv("OPENAI_API_KEY")
api_token = os.getenv('TELEGRAM_API_TOKEN')

bot = telegram.Bot(token=api_token)

app = Flask(__name__)

def set_webhook():
    url = "https://api.telegram.org/bot{}/setWebhook".format(api_token)
    # Set the webhook to the URL of your Flask app
    response = requests.post(url, data={'url': 'https://renegade.herokuapp.com/hook'})
    print(response.status_code)

if __name__ == "__main__":
    set_webhook()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

conversation = []
conversation = load_conversation_log()
log_conversation(conversation)

@app.route('/hook', methods=['POST'])
def webhook_handler():
    # Get the update from Telegram
    update = telegram.Update.de_json(request.get_json(force=True), bot)
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
