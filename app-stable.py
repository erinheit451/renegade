import os
import openai
from flask import Flask, request, Response, redirect, render_template, url_for
from prompt import prompt
from response import generate_chatbot_response
from chatlog import log_conversation, load_conversation_log, prune_conversation_log
from record import log_permanent_record, load_permanent_record


openai.api_key = os.getenv("OPENAI_API_KEY")
app = Flask(__name__)

conversation = []
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
