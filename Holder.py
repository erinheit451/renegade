import os
import openai
from flask import Flask, request
from dotenv import load_dotenv
from twilio.rest import Client

# Load.env 
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

openai.api_key = OPENAI_API_KEY

chatlog = []

def handle_incoming_message(sender, body):
    global chatlog
    chatlog.append({"sender": sender, "body": body})

    # Calc max size of chatlog in tokens
    prompt_size = len(openai.Completion.create(engine="text-davinci-003", prompt="").text)
    max_size = 4096 - prompt_size  # Maximum size of the chatlog in tokens

    # Prune chatlog to remove older messages if needed
    chatlog_size = sum(len(message["body"]) for message in chatlog)
    while chatlog_size > max_size:
        chatlog_size -= len(chatlog.pop(0)["body"])

    # Make a response with openai
    prompt = "\n".join(f"{message['sender']}: {message['body']}" for message in chatlog)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=200,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Send back to send as sms
    client.messages.create(
        to=sender,
        from_=TWILIO_PHONE_NUMBER,
        body=response.text
    )

load_dotenv()

app = Flask(__name__)

# Twilio webhook
@app.route("/sms", methods=["POST"])
def incoming_sms():
  sender = request.form["From"]
  body = request.form["Body"]
  handle_incoming_message(sender, body)
  return "OK"

if __name__ == "__main__":
  app.run()
