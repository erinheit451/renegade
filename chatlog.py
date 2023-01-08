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

def prune_conversation_log(conversation, max_tokens=300):
    while len(conversation) > max_tokens:
        conversation.pop(0)
    return conversation

