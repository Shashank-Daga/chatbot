import tkinter as tk
from tkinter import scrolledtext
import os
import google.generativeai as ai
from dotenv import load_dotenv
import threading

load_dotenv()

api = os.getenv("API_Key")

# configure api
ai.configure(api_key=api)

# Create a model
model = ai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat()


def send_message():
    user_input = entry.get().strip()
    if user_input:
        chatbox.insert(tk.END, "You: " + user_input + "\n", "user")
        entry.delete(0, tk.END)
        chatbox.yview(tk.END)  # Auto-scroll to the latest message

        threading.Thread(target=get_response, args=(user_input,), daemon=True).start()


def get_response(user_input):
    # Replace this with AI chatbot integration (e.g., OpenAI, custom NLP model)
    # Conversation
    response = chat.send_message(user_input)
    chatbox.insert(tk.END, "Bot: " + response.text + "\n\n", "bot")
    chatbox.yview(tk.END)
    # print("Chatbot: ", response.text)
    # return response.text


# Create the main window
root = tk.Tk()
root.title("AI Chatbot")
root.geometry("550x550")

# Chat display area
chatbox = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, font=("Arial", 12))
chatbox.pack(padx=10, pady=10)
chatbox.tag_config("user", foreground="blue")
chatbox.tag_config("bot", foreground="green")

# Entry field
entry = tk.Entry(root, width=50, font=("Arial", 12))
entry.pack(padx=10, pady=5, side=tk.LEFT)

# Send button
send_button = tk.Button(root, text="Send", command=send_message, font=("Arial", 12), bg="lightblue")
send_button.pack(pady=5, side=tk.RIGHT)

# Run the application
root.mainloop()
