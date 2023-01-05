import json

def log_conversation(user_input, chatbot_response):
    conversation = {
        "user_input": user_input,
        "chatbot_response": chatbot_response
    }
    with open("chatlog.json", "a") as f:
        json.dump(conversation, f)
        f.write("\n")
    f.close()
