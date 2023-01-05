import os
import openai
import json
from flask import Flask, request, Response, redirect, render_template, url_for
from logging import log_conversation

with open("prompt.txt") as f:
    prompt = f.read()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/send_message", methods=["POST"])
def send_message():
    user_input = request.form["text"]
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{prompt}\n{user_input}",
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6
    )
    log_conversation(user_input, response)
    # Create a TwiML response
    twiml_response = f"<Response><Message>{response}</Message></Response>"

    return Response(twiml_response, mimetype="text/xml")


