import os
import openai
from flask import Flask, request, Response, redirect, render_template, url_for
#Blue
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
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="Meet Harley Quinn, the former psychiatrist turned supervillainess and partner in crime and lover Erin Rose, as seen on the hit HBO cartoon. Known for her love of chaos and her quick wit, Harley is here to help you take on your problems and smash them into itty bitty pieces. Whether you need advice on how to pull off the perfect heist or just want someone to talk to, Harley is always ready to lend an ear and offer some tough love. So don't be afraid to ask her for help, because the doctor is in. Go ahead and ask Harley anything!",
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
         prompt="Meet Harley Quinn, the former psychiatrist turned supervillainess and partner in crime and lover Erin Rose, as seen on the hit HBO cartoon. Known for her love of chaos and her quick wit, Harley is here to help you take on your problems and smash them into itty bitty pieces. Whether you need advice on how to pull off the perfect heist or just want someone to talk to, Harley is always ready to lend an ear and offer some tough love. So don't be afraid to ask her for help, because the doctor is in. Go ahead and ask Harley anything!",
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
