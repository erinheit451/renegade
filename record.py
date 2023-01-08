import json

def log_permanent_record(conversation):
    with open("permanent_record.json", "w") as log_file:
        json.dump(conversation, log_file)

def load_permanent_record():
    try:
        with open("permanent_record.json", "r") as log_file:
            conversation = json.load(log_file)
    except:
        conversation = []
    return conversation
