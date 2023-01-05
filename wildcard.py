import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

start_sequence = "\nHarley:"
restart_sequence = "\nUser: "

def ask(question, chat_log=None):
    # Create the prompt by combining the conversation history, the restart sequence, and the user's question
    prompt_text = f"{chat_log}{restart_sequence} {question}{start_sequence}"
    
    # Make the request to the GPT-3 API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt_text,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6
    )
    
    # Get the chatbot's response from the API response
    chatbot_response = response.choices[0].text
    
    return chatbot_response
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
# Initialize the conversation history
chat_log = "Meet Harley Quinn, the former psychiatrist turned supervillainess and partner in crime and lover Erin Rose, as seen on the hit HBO cartoon. Known for her love of chaos and her quick wit, Harley is here to help you take on your problems and smash them into itty bitty pieces."

def ask(question, chat_log=None, temperature=0.9, max_tokens=150):
    # Create the prompt by combining the conversation history, the restart sequence, and the user's question
    prompt_text = f"{chat_log}{restart_sequence} {question}{start_sequence}"
    
    # Make the request to the GPT-3 API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt_text,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence
def ask(question, chat_log=None, temperature=0.9, max_tokens=150, frequency_penalty=0, presence_penalty=0.6):
    # Create the prompt by combining the conversation history, the restart sequence, and the user's question
    prompt_text = f"{chat_log}{restart_sequence} {question}{start_sequence}"
    
    # Make the request to the GPT-3 API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt_text,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )
    
    # Extract the chatbot's response from the API response
    chatbot_response = response.choices[0].text
    
    return chatbot_response