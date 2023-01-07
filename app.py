import os
import openai
from flask import Flask, request
from dotenv import load_dotenv
from twilio.rest import Client
load_dotenv()

# Load secure info from .env file
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set up Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Set up OpenAI API client
openai.api_key = OPENAI_API_KEY

# Initialize chatlog
chatlog = []

def handle_incoming_message(sender, body):
  global chatlog

  # Add the incoming message to the chatlog
  chatlog.append({"sender": sender, "body": body})

  # Calculate the maximum size of the chatlog in tokens
  try:
    prompt_size = len(openai.Completion.create(model="text-davinci-003", prompt="").text)
  except openai.api_errors.ApiException as e:
    print("An error occurred when calling the OpenAI API:")
    print(e)
    print(f"prompt_size = {prompt_size}")
    return

  max_size = 4096 - prompt_size  # Maximum size of the chatlog in tokens

  # Prune the chatlog to remove older messages if needed
  chatlog_size = sum(len(message["body"]) for message in chatlog)
  while chatlog_size > max_size:
    chatlog_size -= len(chatlog.pop(0)["body"])

  # Use the OpenAI API to generate a response to the incoming message
  prompt = "\n".join(f"{message['sender']}: {message['body']}" for message in chatlog)
  try:
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt,
      temperature=0.7,
      max_tokens=200,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
  except openai.api_errors.ApiException as e:
    print("An error occurred when calling the OpenAI API:")
    print(e)
    return

  # Send the response back to the sender as an SMS message
  client.messages.create(
    to=sender,
    from_=TWILIO_PHONE_NUMBER,
    body=response.text
  )

# Create a Flask app
app = Flask(__name__)

# Set up a Twilio webhook to listen for incoming messages
@app.route("/sms", methods=["POST"])
def incoming_sms():
  sender = request.form["From"]
  body = request.form["Body"]
  handle_incoming_message(sender, body)
  return "OK"

if __name__ == "__main__":
  app.run()
