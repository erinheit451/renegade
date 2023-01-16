import os
import openai
import telegram
from flask import Flask, request, Response, redirect, render_template, url_for
from prompt import prompt

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
bot_token = os.environ["BOT_TOKEN"]
bot = telegram.Bot(token=bot_token)
conversation = []

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
@app.route("/webhook", methods=["POST"])
def webhook():
    # Get the update from Telegram
    update = request.get_json()

    # Get the message text
    message_text = update.message.text

    # Generate a response using the OpenAI GPT-3 API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=message_text,
        max_tokens=250,
        temperature=0.7
    )

    # Send the response to Telegram
    bot.send_message(chat_id=update.effective_chat.id, text=response["choices"][0]["text"])

    # Return a 200 OK response
    return "OK"

# Set the webhook
bot.setWebhook(url='https://renegade.herokuapp.com/webhook')

