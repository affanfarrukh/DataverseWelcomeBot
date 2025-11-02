# run_nova.py

import os
from dotenv import load_dotenv
from welcome_bot import bot  # Import the bot instance from welcome_bot.py

# Load the environment variables from your .env file
load_dotenv()

# Fetch your Discord bot token
token = os.getenv("Nova_Bot_Token")

if not token:
    raise ValueError("❌ Nova_Bot_Token not found in .env file! Make sure it's defined in your .env file.")

print("🚀 Starting Nova...")

# Run the bot
bot.run(token)
