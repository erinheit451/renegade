def sms():
    # Get the message body from the request
    body = request.form["Body"]

    # Generate a response
    chatbot_response = generate_response(f"{prompt}{body}")

    # Create a TwiML response
    twiml_response = f"<Response><Message>{chatbot_response}</Message></Response>"

    return Response(twiml_response, mimetype="text/xml")
