import json

def write_conversation_to_file(user_input, chatbot_response):
    # Set the maximum number of conversations to keep
    max_conversations = 100

    # Open the file in append mode
    with open("conversations.json", "a") as file:
        # Read the existing conversations from the file
        file.seek(0)
        conversations = json.load(file)

        # Check if the number of conversations exceeds the maximum allowed
        if len(conversations) > max_conversations:
            # Keep only the most recent conversations
            conversations = conversations[-max_conversations:]

            # Rewrite the file with the truncated list of conversations
            file.seek(0)
            file.truncate()
            json.dump(conversations, file)

        # Add the new conversation to the list of conversations
        conversations.append({"user": user_input, "chatbot": chatbot_response})

        # Write the updated list of conversations to the file
        file.seek(0)
        file.truncate()
        json.dump(conversations, file)
