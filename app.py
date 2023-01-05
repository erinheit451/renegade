import os
import openai

# Read the prompt from a file
with open("prompt.txt") as f:
    prompt = f.read()

# Set the maximum conversation length
MAX_CONVERSATION_LENGTH = 100

# Initialize the conversation history
conversation = []

@app.route("/sms", methods=["POST"])
def sms():
    # Get the message body from the request
    body = request.form["Body"]

    # Check for the special command
    if body.lower() == "reset chat log":
        conversation.clear()  # Clear the conversation history
        chatbot_response = "Chat log reset."  # Set the chatbot's response
    else:
        # Generate a response
        chatbot_response = openai.Completion.create(engine="text-davinci-003", prompt=f"{prompt}\n{'\n'.join([message for sender, message in conversation])}\n{body}", temperature=0.9, max_tokens=150).text

        # Store the conversation in the deque
        conversation.append({"user": body})
        conversation.append({"chatbot": chatbot_response})

        # Save the conversation to a file
        with open("chatlog.txt", "w") as f:
            f.write("\n".join([f"{sender}: {message}" for sender, message in conversation]))

    # Create a TwiML response
    twiml_response = f"<Response><Message>{chatbot_response}</Message></Response>"

    return Response(twiml_response, mimetype="text/xml")

@app.route("/startup", methods=["GET"])
def startup():
    # Send the "I'm awake" message
    send_message("I'm awake!")

    # Redirect the user to the chat log page
    return redirect(url_for("chatlog"))

@app.route("/chatlog", methods=["GET"])
def chatlog():
    # Read the chat log file
    with open("chatlog.txt") as f:
        chatlog = f.read()

    # Render the chat log template
    return render_template("chatlog.html", chatlog=chatlog)

def send_message(message):
    # Read the Twilio API credentials from the .env file
    twilio_sid = os.getenv("TWILIO_SID")
    twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_FROM_NUMBER")

    # Send the message using the Twilio API
    client = Client(twilio_sid, twilio_auth_token)
    client.messages.create(body=message, from_=from_number, to=to_number)
