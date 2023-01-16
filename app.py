import os
import openai
import telegram
import logging
from prompt import prompt
from flask import Flask, request, Response, redirect, render_template, url_for
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters
from telegram import Update


app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
bot_token = os.environ["BOT_TOKEN"]
bot = telegram.Bot(token=bot_token)

@app.route("/", methods=("GET", "POST"))
def index():

    #kill
    return
    
    global conversation
    # Handle form submission
    if request.method == "POST":
        user_input = request.form["input"]
        conversation.append({"user": user_input})
        # Generate a response from the chatbot
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"{prompt}{user_input}",
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6
    )

        chatbot_response = response.choices[0].text
        conversation.append({"chatbot": chatbot_response})
    return render_template("index.html", conversation=conversation)

@app.route("/sms", methods=["POST"])
def sms():
    # Get the message body from the request
    body = request.form["Body"]
    # Generate a response
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{prompt}{body}",
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6
    )

    chatbot_response = response.choices[0].text
    # Create a TwiML response
    twiml_response = f"<Response><Message>{chatbot_response}</Message></Response>"
    return Response(twiml_response, mimetype="text/xml")

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
    context = CallbackContext(dispatcher)
    if 'message' in update:
        handle_text(update, context)
    return "OK"


updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.text, handle_text))

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

updater.start_polling()

if __name__ == '__main__':
    app.run()
