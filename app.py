import os
import openai
import telegram
import requests
import dotenv
import chatlog
from flask import Flask, request, Response, render_template
from prompt import prompt
from response import generate_chatbot_response
from chatlog import log_conversation, load_conversation_log, prune_chatlog
from record import log_permanent_record, load_permanent_record

openai.api_key = os.getenv("OPENAI_API_KEY")
dotenv.load_dotenv()
bot = telegram.Bot(token=os.environ['TELEGRAM_BOT_TOKEN'])

app = Flask(__name__)

conversation = load_conversation_log()
log_conversation(conversation)


@app.route("/", methods=["POST"])
def index():
    global conversation
    # Handle form submission
    if request.method == "POST":
        user_input = request.form["input"]
        conversation.append({"user": user_input})
        # Prune the conversation to ensure it doesn't exceed the maximum number of tokens
        conversation = prune_chatlog(conversation, 300)
        # Generate a chatlog by pruning the conversation
        chatlog = prune_chatlog(conversation)
        chatbot_response = generate_chatbot_response(prompt, user_input, chatlog)
        conversation.append({"chatbot": chatbot_response})
    return render_template("index.html", conversation=conversation)

@app.route("/sms", methods=["POST"])
def sms():
    global conversation
    # Get the message body from the request
    body = request.form["Body"]
    # Prune the conversation to ensure it doesn't exceed the maximum number of tokens
    conversation = prune_chatlog(conversation, 300)
    # Generate a response
    chatlog = prune_chatlog(conversation)
    chatbot_response = generate_chatbot_response(prompt, body, chatlog)
    conversation.append({"chatbot": chatbot_response})
    # Create a TwiML response
    twiml_response = f"<Response><Message>{chatbot_response}</Message></Response>"
    return Response(twiml_response, mimetype="text/xml")
