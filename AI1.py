import os

import google.generativeai as ai
from dotenv import load_dotenv

load_dotenv()

api = os.getenv("API_Key")

# configure api
ai.configure(api_key=api)

# Create a model
model = ai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat()

# Conversation
while True:
    msg = input('You: ')

    if msg.lower() == "bye":
        print("Bye!")
        break

    response = chat.send_message(msg)
    print("Chatbot: ", response.text)
