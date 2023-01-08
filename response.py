import os
import openai
from flask import Flask, request, Response, redirect, render_template, url_for
from prompt import prompt

def generate_chatbot_response(prompt: str, user_input: str, chatlog: str) -> str:
    history = chatlog + "\n" + user_input
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{prompt}\n{history}",
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6
    )
    chatbot_response = response.choices[0].text
    return chatbot_response


