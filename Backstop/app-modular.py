import os
import openai
from flask import Flask, request, Response, redirect, render_template, url_for

# Import the desired value from prompt.py
from prompt import prompt

# Import the generate_response function from response.py
from response import generate_response

# Import the sms function from sms.py
from sms import sms

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

conversation = []

@app.route("/", methods=("GET", "POST"))
def index():
   
    global conversation

    # Handle form submission
    if request.method == "POST":
        user_input = request.form["input"]
        conversation.append({"user": user_input})

        # Generate a response from the chatbot
        chatbot_response = generate_response(f"{prompt}\n{user_input}")
        conversation.append({"chatbot": chatbot_response})


    # Return the rendered template
    return render_template("index.html", conversation=conversation)

@app.route("/sms", methods=["POST"])
def sms():
    # Get the message body from the request
    body = request.form["Body"]

    # Generate a response
    chatbot_response = generate_response(f"{prompt}{body}")

    # Create a TwiML response
    twiml_response = f"<Response><Message>{chatbot_response}</Message></Response>"

    return Response(twiml_response, mimetype="text/xml")
