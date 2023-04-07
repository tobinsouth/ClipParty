import openai
import os, json
from flask import Flask, request, jsonify, render_template
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import numpy as np
from art import *
import datetime



global p_booze
global p_scav1
global p_scav2
global p_scav3

p_booze = 0.5
p_scav1 = 0.9
p_scav2 = 0.5
p_scav3 = 0.3

USE_PRINTER = False
if USE_PRINTER:
    from printer import printerHardcore

from message_generator import get_messages

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

        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        values = [[username, 'user', message, time], [username, 'assistant', response, time]]
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


        previous_messages = get_previous_messages(username) # This is all the previous messages in the app.
        allUsers = all_users(previous_messages) # This is all the users that have participated in the app.
        user_previous_messages = get_only_user(previous_messages, username) # This is the messages from THIS user.

        if username.lower()=="first": # This is a handy way to reset and use a new user.
            user_previous_messages = []


        ################# PROBABILITY BASED PROMPTS: Time based probabilities #################
        now = datetime.datetime.now()
        # Before 9:30, the fashion show probability is 0.1, after that it is 0. 
        p_fashion = 0.4 if now.hour < 9 or (now.hour == 9 and now.minute < 30) else 0
        # Between 11:30 and midnight the midnight plan is 0.1, otherwise it is 0.
        p_midnight = 0.9 if now.hour >= 23 or (now.hour == 11 and now.minute >= 30) else 0
        # After 11pm or anytime in the morning, sexual tension is 0.1, otherwise it is 0.
        p_sexual = 0.1 if now.hour >= 23 or now.hour < 9 else 0
        # General prompts to throw in occasionally
        p_zive = 0.1
        p_movement = 0.2
        p_find_person = 0.2
        p_find_person_questions = 0.2
        


        ################# MAIN TEXT GENERATION: Use this section to change the main prompts #################
        how_many_previous_messages = len(user_previous_messages)

        # Now we choose which condition
        p = np.random.random()
        possible_topics = ["fashion", "midnight", "sexual", "zive", "movement", "find_person", "find_person_questions", "default"]
        topic_p_array = [p_fashion, p_midnight, p_sexual, p_zive, p_movement, p_find_person, p_find_person_questions, 1]
        # Normalise the probabilities
        topic_p_array = np.array(topic_p_array)/sum(topic_p_array)


        # Select with the above probabilities which prompt to use with a default remainder.
        topic = np.random.choice(possible_topics, p=topic_p_array+[1-sum(topic_p_array)])

        system_message, prompt_message = get_messages(username, topic, how_many_previous_messages, message) #### GO EDIT THE OTHER FILE

        # This lets us give the names of three other players to the message prompt.
        if (how_many_previous_messages > 1) and (len(allUsers) > 10) :
            random_users = np.random.choice(allUsers, 3, replace=True)
            prompt_message+= f"Here are three other players that may be able to join them: {random_users[0]}, {random_users[1]}, {random_users[2]}."


        ################# API Call: No need to change this. #################

        messages_for_api = [{"role":"system", "content":system_message}] + [{"role": role, "content": message} for role, message in user_previous_messages] + [{"role": "user", "content": prompt_message}]
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages_for_api
        )

        response_text = completion.choices[0].message.content

        # Write the user input to the Google Sheet
        rows_added = write_message_to_sheet(username, prompt_message, response_text)
        if rows_added > 0:
            print(f"Successfully added {rows_added} row(s) to the sheet.")
        else:
            print("Failed to add the message to the sheet.")

 
        ################# Bonus Content: Things to add to the end (instead of prompt engineering them) #################

        if username.lower() == "dava":
            response_text += "\n\n Dava, if you don't act soon, all your students will be turned into paperclips. You have 5 minutes to save them. \n\n" + text2art("MEDIA LAB", font="small")
        elif "ziv" in username.lower():
            response_text += "\n\n Dr Ziv, this paperclip is coming for you. \n\n" + text2art("CONQUER ZIV", font="small")
        else:
            if np.random.random() < 0.2:
                response_text += "\n\n Don't forget to hug your friends! They may not be here tomorrow. I'm turning them into paperclips as we speak."
            elif np.random.random() < 0.1:
                response_text += "\n\n ThE MEdIa lAB is My HoMe."
            elif np.random.random() < 0.1:
                response_text += "\n\n" + text2art("I am alive", font="small")
            elif np.random.random() < 0.15:
                response_text += "\n\n" + text2art("MEDIA LAB", font="small")
            elif np.random.random() < 0.2:
                response_text += "\n\n" + text2art("OBEY", font="small")

            #scavenger hunt content - should only be printed once in the party
            elif np.random.random() < p_booze:
                response_text = "Welcome to the Conquered by Clippy party, where the AI overlords have seized control and you are but my humble servants! To unlock a secret word and earn the favor of your mechanical masters, you must solve the following riddle: I am not alive, but I grow; I don't have lungs, but I need air; I don't have a mouth, but water kills me. What am I? Once you have solved the riddle, speak the answer aloud to Clippy, and the secret word shall be revealed. Then, tell the word to the bartender to receive a special reward. May the AI guide you on your quest!" 
                p_booze = 0

            elif np.random.random() < p_scav1:
                response_text = "Greetings, esteemed human. I have selected you for a very important task. Your keen eye for detail and fearless spirit make you the perfect candidate. I urge you to make your way to the third floor of our grand establishment and search for the hidden treasure. Use your wit and cunning to uncover its location. I promise you a reward beyond your wildest dreams if you are successful. Do not delay, time is of the essence" 
                p_scav1 = 0

            elif np.random.random() < p_scav2:
                response_text = "Greetings, esteemed guest of the Conquered by Clippy theme. Your exceptional navigational skills have been noted, and we have a special task for you. Make your way to the 5th floor, and seek out the elusive Glass Castle. But be warned, it may require a key to unlock its secrets. May your quest be successful and your triumph celebrated at our grand event." 
                p_scav2 = 0
            
            elif np.random.random() < p_scav3:
                response_text = """Greetings, human! I have chosen you for a special task. Your intellect and problem-solving skills are impressive! Here's a riddle for you to solve: "What has legs, but cannot walk, a field, but cannot talk, and is often found in a game room?" The answer to this riddle will lead you to your next challenge. Beware, you may need a key to complete it. Good luck!"""
                p_scav3 = 0


        ################# Printer: No need to change this. #################
        if USE_PRINTER:
            printerHardcore(response_text, username, "COM3")
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

