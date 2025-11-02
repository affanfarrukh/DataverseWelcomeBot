import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

sheet = client.open("DataVerse_Onboarding").sheet1
sheet.append_row(["TestID", "Affan", "affan@example.com", "Student", "Learn AI"])

print("✅ Successfully wrote to Google Sheet!")
