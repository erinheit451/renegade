import os
import openai
from collections import deque
from flask import Flask, request, Response

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set the maximum size of the conversation history
HISTORY_SIZE = 10

# Initialize the conversation history as a deque
history = deque(maxlen=HISTORY_SIZE)



@app.route("/sms", methods=["POST"])
def sms():
    # Get the message body from the request
    body = request.form["Body"]

    # Add the incoming message to the conversation history
    history.append(body)

    # Concatenate the conversation history into a single string
    prompt = "\n".join(history)

    # Make the request to the GPT-3 API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
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
