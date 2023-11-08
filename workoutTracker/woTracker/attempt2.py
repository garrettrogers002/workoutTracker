import os.path
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SPREADSHEET_ID = '1uUJN2HeYXJ1NdPFD4BGXK3XYwPjT2SWt--rgfUTJ_VU'

day = input('What day was it today? '.lower())
if day == 'leg':
    exercises = 


def get_next_available_row(sheet_name, service):
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=f'{sheet_name}!A1:A').execute()
    values = result.get('values', [])
    return len(values) + 1

def main():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        today = datetime.now().strftime('%Y-%m-%d')
        sheet_name = f'{day}'

        next_row = get_next_available_row(sheet_name, service)
        range_name = f'{sheet_name}!A{next_row}:D{next_row}'

        values = [[today, sqWeight, '3', '6']]

        body = {'values': values}
        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID, range = range_name,
            valueInputOption = 'RAW', body=body).execute()
        print('{0} cells updated.'.format(result.get('updatedCells')))

    except HttpError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()