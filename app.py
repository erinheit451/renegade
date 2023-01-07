import os
import openai
from flask import Flask, request, Response, redirect, url_for
from prompt import prompt

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

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