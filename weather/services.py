import os
import requests
import json
import pandas as pd
import dotenv 
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

dotenv.load_dotenv()

OPEN_WEATHER_KEY = os.getenv('OPEN_WEATHER_KEY')

def get_lat_lon(city_name, state_code, country_code): 
    r = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&appid={OPEN_WEATHER_KEY}').json()
    data = r[0]
    lat, lon = data['lat'], data['lon']
    return lat, lon

def get_current_weather(lat, lon): 
    r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPEN_WEATHER_KEY}&units=imperial').json()
    return r

def get_google_sheet(): 
    # This function is based off of the Google Workspace python quickstart guide: 
    # https://developers.google.com/sheets/api/quickstart/python#configure_the_sample
    
    # If modifying these scopes, delete the file token.json.
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = "1_Rxr-2jkJgWmmO6xLJJ61SHEXeRCUVIgv6cXXnvz438"
    SAMPLE_RANGE_NAME = "Cities"

    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=8000)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
            .execute()
        )
        values = result.get("values", [])

        if not values:
            print("No data found.")
            return

        data = []
        for row in values:
            data.append(row)
        df = pd.DataFrame(data, columns = data[0])
        return df
    except HttpError as err:
        print(err)



# data_list = get_google_sheet()
# print(data_list)
# print(len(data_list))