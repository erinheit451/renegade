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

def prune_chatlog(chatlog: str, max_tokens: int) -> str:
    tokens = chatlog.split()
    while len(tokens) > max_tokens:
        # Split the chatlog into lines
        lines = chatlog.split("\n")
        # Remove the oldest message (the first line)
        lines.pop(0)
        # Join the lines back into a single string
        chatlog = "\n".join(lines)
        # Update the list of tokens
        tokens = chatlog.split()
    return chatlog

