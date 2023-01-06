def index():
   
    global conversation

    # Handle form submission
    if request.method == "POST":
        user_input = request.form["input"]
        conversation.append({"user": user_input})

        # Generate a response from the chatbot
        chatbot_response = generate_response(f"{prompt}\n{user_input}")
        conversation.append({"chatbot": chatbot_response})

    # Return the rendered template
    return render_template("index.html", conversation=conversation)
