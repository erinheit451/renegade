import json

def log_conversation(conversation):
    with open("conversation_log.json", "w") as log_file:
        json.dump(conversation, log_file)

def load_conversation_log():
    try:
        with open("conversation_log.json", "r") as log_file:
            conversation = json.load(log_file)
    except:
        conversation = []
    return conversation

def prune_conversation_log(conversation_log):
    conversation_str = ""
    for message in conversation_log:
        if "user" in message:
            conversation_str += f"USER: {message['user']}\n"
        elif "chatbot" in message:
            conversation_str += f"CHATBOT: {message['chatbot']}\n"
    return conversation_str

