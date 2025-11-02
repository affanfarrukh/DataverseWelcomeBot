# store_user_data.py
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SHEET_NAME = "DataVerse_Onboarding"  # your Google Sheet name
SERVICE_ACCOUNT_FILE = "credentials.json"  # service account key path


def get_google_sheet():
    """Authenticate and return the Google Sheet object."""
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).sheet1
    return sheet


def save_user_data(user_data: dict):
    """
    Save user data into JSON file and append it to Google Sheet
    — but only if this Discord user doesn't already exist.
    """
    try:
        # --- Save locally as JSON (always append for backup) ---
        file_path = "onboarding_data.json"
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        data.append(user_data)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"✅ Stored user data locally for {user_data.get('name')}")

        # --- Google Sheet Handling ---
        sheet = get_google_sheet()
        existing_records = sheet.get_all_records()

        # Extract all Discord IDs already in the sheet
        existing_ids = [str(row.get("ID") or row.get("id")) for row in existing_records]

        if str(user_data.get("discord_id")) in existing_ids:
            print(f"⚠️ User {user_data.get('name')} ({user_data.get('discord_id')}) already exists in sheet. Skipping.")
            return  # Stop here, no duplicate row added

        # If not found → append as new row
        sheet.append_row([
            user_data.get("discord_id"),
            user_data.get("name"),
            user_data.get("email"),
            user_data.get("role"),
            user_data.get("goal"),
        ])
        print(f"✅ Added {user_data.get('name')} to Google Sheet.")

    except Exception as e:
        print(f"❌ Error while saving user data: {e}")
