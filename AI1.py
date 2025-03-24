import customtkinter as ctk
import os
import google.generativeai as ai
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("API_Key")

if not api_key:
    print("API Key is missing! Set it in the environment variables.")
    exit()

# Configure Gemini AI
ai.configure(api_key=api_key)
model = ai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat()

# Global variable to track theme
current_theme = "dark"


# Function to update text colors dynamically
def update_text_colors():
    if current_theme == "dark":
        chat_log.tag_config("user", foreground="cyan")
        chat_log.tag_config("bot", foreground="lightgreen")
    else:
        chat_log.tag_config("user", foreground="darkblue")
        chat_log.tag_config("bot", foreground="darkgreen")


# Function to handle sending messages
def send_message():
    user_message = user_input.get().strip()

    if not user_message:
        return  # Ignore empty messages

    chat_log.insert("end", f"You: {user_message}\n", "user")
    user_input.delete(0, "end")  # Clear input field

    if user_message.lower() == "bye":
        chat_log.insert("end", "Chatbot: Bye!\n", "bot")
        root.quit()
        return

    try:
        response = chat.send_message(user_message)
        chat_log.insert("end", f"Chatbot: {response.text}\n", "bot")
    except Exception as e:
        chat_log.insert("end", "Chatbot: Error fetching response.\n", "bot")
        print("Error:", e)

    chat_log.yview("end")  # Auto-scroll to latest message


# Function to toggle theme
def toggle_theme():
    global current_theme
    if current_theme == "dark":
        ctk.set_appearance_mode("light")
        theme_button.configure(text="🌙 Dark Mode")
        current_theme = "light"
    else:
        ctk.set_appearance_mode("dark")
        theme_button.configure(text="☀️ Light Mode")
        current_theme = "dark"

    update_text_colors()  # Apply new colors


# UI Setup
ctk.set_appearance_mode(current_theme)  # Default to dark mode
root = ctk.CTk()
root.title("Chatbot")
root.geometry("600x500")

# Heading
heading_label = ctk.CTkLabel(root, text="What can I help with?", font=("Arial", 18, "bold"))
heading_label.pack(pady=15)

# Chat log area
chat_log = ctk.CTkTextbox(root, width=550, height=300, wrap="word", font=("Arial", 12))
chat_log.pack(pady=10)

# Apply initial text colors
update_text_colors()

# Input field frame
input_frame = ctk.CTkFrame(root)
input_frame.pack(pady=10, padx=10, fill="x")

user_input = ctk.CTkEntry(input_frame, placeholder_text="Ask anything...", width=450, font=("Arial", 14))
user_input.pack(side="left", padx=10, pady=5, expand=True)

send_button = ctk.CTkButton(input_frame, text="➤", width=50, font=("Arial", 16), command=send_message)
send_button.pack(side="right", padx=10)

# Theme toggle button
theme_button = ctk.CTkButton(root, text="☀️ Light Mode", command=toggle_theme)
theme_button.pack(pady=10)

# Start GUI
root.mainloop()
