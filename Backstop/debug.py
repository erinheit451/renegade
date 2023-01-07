import os
import openai
from flask import Flask, request, Response, redirect, render_template, url_for
# Import the desired value from prompt.py
from prompt import prompt

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

conversation = []

def handle_form_submission(user_input):
    # Generate a response from the chatbot
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{prompt}\n{user_input}",
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
   
    global conversation

    # Handle form submission
    if request.method == "POST":
        user_input = request.form["input"]
        conversation.append({"user": user_input})

        # Generate a response from the chatbot
        chatbot_response = handle_form_submission(user_input)
        conversation.append({"chatbot": chatbot_response})

    # Return the rendered template
    return render_template("index.html", conversation=conversation)

if __name__ == "__main__":
    # Test the handle_form_submission function
    print(handle_form_submission("Hello, chatbot!"))

    # Test the render_template function
    print(render_template("index.html", conversation=conversation))
