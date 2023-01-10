import os
import openai
import telegram
import asyncio

openai.api_key = os.getenv("OPENAI_API_KEY")

bot = telegram.Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))

async def main():
    # Get the chat id
    updates = await bot.get_updates()
    chat_id = updates[-1].message.chat.id

    # Generate a response using OpenAI's Completion API
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="Hello, I'm Harley Quinn, supervillianess with a heart of gold. What's up?",
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6
        )
        message = response.choices[0].text
    except Exception as e:
        message = "Sorry, something went wrong when generating a response."

    # Send the message to the user
    bot.send_message(chat_id=chat_id, text=message)

asyncio.run(main())


