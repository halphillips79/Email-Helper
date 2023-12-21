# emailhelper2/views.py

import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
import logging

from django.shortcuts import render
from django.http import HttpResponse

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Define the Google Sheets spreadsheet name
spreadsheet_name = "PLACEHOLDER Shift / Class Coverage Form (Responses)"

# Define the credentials JSON file path
credentials_file = "credentials.json"

# Set up the scope and credentials
scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scopes)
client = gspread.authorize(credentials)

def update_spreadsheet():
    # Open the Google Sheets spreadsheet
    logging.debug("Opening Google Sheets spreadsheet...")
    spreadsheet = client.open(spreadsheet_name)

    # Get the first sheet of the spreadsheet
    worksheet = spreadsheet.worksheet("Form Responses 1")

    # Read the data from the worksheet into a DataFrame
    logging.debug("Reading data from the worksheet...")
    df = pd.DataFrame(worksheet.get_all_records())

    messages = []

    # Iterate over the rows in the DataFrame
    for index, row in df.iterrows():
        shift_class = row['What type of coverage are you submitting?']
        date = row['What date is being covered?']
        name1 = row['What is the first and last name of the person who will be covering this shift / class?']
        name2 = row['What is the first and last name of the person who normally covers this shift / teaches this class?']
        class_foh_shift_tech_shift = row['What type of coverage are you submitting?']
        start_time = row['What time does the covered shift/class begin?']
        end_time = row['What time does the covered shift/class end?']
        location = row['At which PLACEHOLDER location does your shift take place?']

        message = f"PLACEHOLDER {shift_class} Coverage {date}\n\n"
        message += f"Hi there - This email is to confirm that {name1} will be covering {name2}'s {class_foh_shift_tech_shift} on {date} "
        message += f"from {start_time} to {end_time} at {location}.\n\n"
        message += "If the above contains any errors or is not what you agreed to, please reach out immediately so that we can revise the schedule.\n\n"
        message += "Best,\n"
        message += "The PLACEHOLDER team"

        messages.append(message)

    # Insert the messages into the "Email text" column at column K, starting from row 2
    logging.debug("Updating the 'Email text' column in the Google Sheets spreadsheet...")
    worksheet.update('K2:K', [[msg] for msg in messages])

    logging.debug("Messages have been inserted into the 'Email text' column of the Google Sheets spreadsheet.")

def button_click(request):
    if request.method == 'POST':
        # Update the spreadsheet
        update_spreadsheet()

        # Return a response indicating the button was clicked successfully
        return HttpResponse("Button clicked successfully")
    
    # For GET requests, render the button.html template
    return render(request, 'button.html')