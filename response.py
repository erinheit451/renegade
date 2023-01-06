
# Import the desired value from prompt.py
from prompt import prompt

# Generate the response and make it a string so it'll work on all platforms
def generate_response(prompt: str) -> str:
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6
    )
    return response.choices[0].text