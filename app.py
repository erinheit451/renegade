import os
import openai
import telegram
import requests
import dotenv
from flask import Flask, request, Response, render_template
from prompt import prompt
from response import generate_chatbot_response
from chatlog import log_conversation, load_conversation_log, prune_conversation_log
from record import log_permanent_record, load_permanent_record

openai.api_key = os.getenv("OPENAI_API_KEY")
dotenv.load_dotenv()
bot = telegram.Bot(token=os.environ['TELEGRAM_BOT_TOKEN'])

app = Flask(__name__)

conversation = load_conversation_log()
log_conversation(conversation)

@app.route("/", methods=("GET", "POST"))
def index():
    global conversation
    # Handle form submission
    if request.method == "POST":
        user_input = request.form["input"]
        conversation.append({"user": user_input})
        # Generate a response from the chatbot
        chatlog = prune_conversation_log(conversation)
        chatbot_response = generate_chatbot_response(prompt, user_input, chatlog)
        conversation.append({"chatbot": chatbot_response})
        log_permanent_record(conversation)
    return render_template("index.html", conversation=conversation)


@app.route("/sms", methods=["POST"])
def sms():
    # Get the message body from the request
    body = request.form["Body"]
    # Generate a response
    chatlog = prune_conversation_log(conversation)
    chatbot_response = generate_chatbot_response(prompt, body, chatlog)
    conversation.append({"chatbot": chatbot_response})
    log_permanent_record(conversation)
    # Create a TwiML response
    twiml_response = f"<Response><Message>{chatbot_response}</Message></Response>"
    return Response(twiml_response, mimetype="text/xml")

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
    # Send the response to the user
    bot.send_message(chat_id=update.message.chat_id, text=chatbot_response)

def set_webhook():
    # Set the webhook
    bot_url = f'https://renegade.herokuapp.com/hook'
    bot.set_webhook(url=bot_url)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    set_webhook()

