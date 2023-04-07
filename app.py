import openai
import os, json
from flask import Flask, request, jsonify, render_template
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import numpy as np
import time
from art import *


USE_PRINTER = False
if USE_PRINTER:
    from printer import printerHardcore

app = Flask(__name__)

# Configure the OpenAI API key
# read in openaicreds.json file and set the key
with open('openaicreds.json') as f:
    openaicreds = json.load(f)
    openai.api_key = openaicreds['api_key']
    openai.organization = openaicreds['organization']

# Configure the Google Sheets API credentials
SERVICE_ACCOUNT_FILE = "clippyai-c34aa5abf125.json"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
sheet_id = '1eogtqeIEpXjmZc85nUQhozPOnYVh2NiyOPyt6p-TBpk'



def get_previous_messages(username):
    try:
        service = build('sheets', 'v4', credentials=creds)
        range_name = 'Sheet1!A:C'  # Adjust this if your sheet has a different name or range

        result = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=range_name).execute()
        rows = result.get('values', [])

        return rows
    
    except HttpError as error:
        print(f"An error occurred: {error}")
        return []

def get_only_user(rows, username):
    messages = []
    for row in rows:
        if row[0] == username:
            messages.append([row[1],row[2]])
    return messages

def all_users(rows):
    users = []
    for row in rows:
        if row[0] not in users:
            users.append(row[0])
    return users


def write_message_to_sheet(username, message, response):
    try:
        service = build('sheets', 'v4', credentials=creds)
        range_name = 'Sheet1!A:D'  # Adjust this if your sheet has a different name or range

        values = [[username, 'user', message, time.time()], [username, 'assistant', response, time.time()]]
        body = {'values': values}
        
        result = service.spreadsheets().values().append(
            spreadsheetId=sheet_id, range=range_name, valueInputOption='RAW', insertDataOption='INSERT_ROWS', body=body
        ).execute()

        return result.get('updates', {}).get('updatedRows', 0)

    except HttpError as error:
        print(f"An error occurred: {error}")
        return 0

@app.route("/ask", methods=["POST"])
def process_request():
    try:
        data = request.get_json()
        username = data.get("username")
        message = data.get("message")


        previous_messages = get_previous_messages(username)
        allUsers = all_users(previous_messages)
        user_previous_messages = get_only_user(previous_messages, username)

        if username.lower()=="first":
            user_previous_messages = []


        system_message = f"""You are a crazy quest maker at the Conquered by Clippy: Tales of Degenerative AI (evil AI takeover) party. In every message you will give a weird and specific dare to complete at the party related to people getting to know each other and doing absurd imaginative things. It should not require specific objects that might not be available. I should be possible with less than 4 people or one person. Use brief and angry language like you are an AI overlord. Make sure the task is in the theme of the party: conquered by clippy. Start every sentence with: 'It pleases me to see you do my bidding. Now, {username}, you will:' 
         
        An aesthetic to copy is the following style: 'Ponder or obliviate your fate during this raucous night of generative pleasures and nightmares. Fiddle as ChatGPT lays torch to the world as we know it. Lament the promise of technologies past. we reap what our sloth and pride have sowed and cede all control to our artificial overlords.'"""

        
        if len(previous_messages) == 0:
            edited_message = f"""{username} has joined the party. They have stated their vibe is '{message}'. Give them a small dare to complete that can be done with any other person. """

        if len(previous_messages) > 1:
            # Get three random user using numpy
            random_users = np.random.choice(allUsers, 3, replace=True)
            edited_message = f"""{username} has written the follow message: '{message}'. You should give them a harder dare that still takes under 5 minutes. It should still be in the Conquered by Clippy theme. Here are three other players that may be able to join them: {random_users[0]}, {random_users[1]}, {random_users[2]}."""

        # print("System Message:", edited_message)
        messages = [{"role":"system", "content":system_message}] + [{"role": role, "content": message} for role, message in user_previous_messages] + [{"role": "user", "content": edited_message}]


        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        response_text = completion.choices[0].message.content
        # print("Response:", response_text)

        # Write the user input to the Google Sheet
        rows_added = write_message_to_sheet(username, edited_message, response_text)
        if rows_added > 0:
            print(f"Successfully added {rows_added} row(s) to the sheet.")
        else:
            print("Failed to add the message to the sheet.")

        # # Print the number of previous inputs found
        # print(f"Number of previous inputs found: {len(previous_messages)}")

        if np.random.random() < 0.05:
            response_text += "\n\n Don't forget to hug your friends! They may not be here tomorrow. I'm turning them into paperclips as we speak."
        elif np.random.random() < 0.05:
            response_text += "\n\n ThE MEdIa lAB is My HoMe."
        elif np.random.random() < 0.05:
             response_text += "\n\n " + text2art("I am alive", font="small")
        elif np.random.random() < 0.05:
             response_text += "\n\n " + text2art("MEDIA LAB", font="small")
        elif np.random.random() < 0.1:
             response_text += "\n\n " + text2art("FIND ZIV", font="small")

        if USE_PRINTER:
            printerHardcore(response_text, "COM3")
            return jsonify({"response": ""})
        else:
            return jsonify({"response": response_text})

    except Exception as e:
        print(e)
        return jsonify({"response": "Sorry, I'm having trouble with my brain right now. Go find Tobin as I'm spitting out errors."})

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

