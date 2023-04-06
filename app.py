import openai
import os, json
from flask import Flask, request, jsonify, render_template
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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

        messages = []
        for row in rows:
            if row[0] == username:
                messages.append([row[1],row[2]])

        return messages

    except HttpError as error:
        print(f"An error occurred: {error}")
        return []


def write_message_to_sheet(username, message, response):
    try:
        service = build('sheets', 'v4', credentials=creds)
        range_name = 'Sheet1!A:C'  # Adjust this if your sheet has a different name or range

        values = [[username, 'user', message], [username, 'assistant', message]]
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
    data = request.get_json()
    username = data.get("username")
    message = data.get("message")

    previous_messages = get_previous_messages(username)



    print("Prompt:", message)


    system_message = f"You are going to be asked a question. Please answer it as if you were talking to a human. The will be asked by someone with the name {username}. Always use this name in creative ways when replying."
    messages = [{"role":"system", "content":system_message}] + [{"role": role, "content": message} for role, message in previous_messages] + [{"role": "user", "content": message}]


    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    response_text = completion.choices[0].message.content
    print("Response:", response_text)

    # Write the user input to the Google Sheet
    rows_added = write_message_to_sheet(username, message, response_text)
    if rows_added > 0:
        print(f"Successfully added {rows_added} row(s) to the sheet.")
    else:
        print("Failed to add the message to the sheet.")

    # Print the number of previous inputs found
    print(f"Number of previous inputs found: {len(previous_messages)}")

    return jsonify({"response": response_text})


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()

