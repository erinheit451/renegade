import os
import openai
import json
from prompt import prompt
from flask import Response
from flask import Flask, request, render_template

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

# Load conversation log from file
try:
    with open("conversation_log.json", "r") as log_file:
        conversation_log = json.load(log_file)
except:
    conversation_log = []

def prune_conversation_log(log, max_tokens=300):
    while len(log) > max_tokens:
        log.pop(0)
    return log

def generate_chatbot_response(prompt, user_input, chatlog):
    history = "\n".join(chatlog + [user_input])
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

@app.route("/", methods=("GET", "POST"))
def index():
    # Handle form submission
    if request.method == "POST":
        user_input = request.form["input"]
        conversation_log.append({"user": user_input})
        # Generate a response from the chatbot
        pruned_log = prune_conversation_log(conversation_log)
        chatbot_response = generate_chatbot_response(prompt, user_input, pruned_log)
        conversation_log.append({"chatbot": chatbot_response})
        # Save the updated conversation log to file
        with open("conversation_log.json", "w") as log_file:
            json.dump(conversation_log, log_file)
        return render_template("index.html", conversation=conversation_log, prompt=prompt)
    else:
        return render_template("index.html", conversation=conversation_log, prompt=prompt)


@app.route("/sms", methods=["POST"])
def sms():
    # Get the message body from the request
    body = request.form["Body"]
    # Generate a response
    pruned_log = prune_conversation_log(conversation_log)
    chatbot_response = generate_chatbot_response(prompt, body, pruned_log)
    conversation_log.append(chatbot_response)
    # Save the updated conversation log to file
    with open("conversation_log.json", "w") as log_file:
        json.dump(conversation_log, log_file)
    # Create a TwiML response
    twiml_response = f"<Response><Message>{chatbot_response}</Message></Response>"
    return Response(twiml_response, mimetype="text/xml")