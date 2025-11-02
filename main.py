import os
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

from welcome_bot import bot  # Import Nova’s logic from welcome_bot.py

# --- Keep-alive web server ---
app = Flask('')

@app.route('/')
def home():
    return "Nova is shining in the Dataverse 🌌"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run).start()

# --- Run Nova ---
if __name__ == "__main__":
    load_dotenv()
    keep_alive()
    token = os.getenv("Nova_Bot_Token")

    if not token:
        raise ValueError("❌ Nova_Bot_Token not found in .env file!")

    bot.run(token)
