import os
import openai
import telegram
from flask import Flask, request

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
bot_token = os.environ["BOT_TOKEN"]
bot = telegram.Bot(token=bot_token)

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
bot.setWebhook(url='https://coaster-amusement-mile.herokuapp.com/webhook')

if __name__ == '__main__':
    app.run()