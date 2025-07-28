import pandas as pd
import numpy as np
import psycopg2
import os
from datetime import datetime

import calendar
import pickle
from openpyxl import load_workbook
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys

import os
import pickle
import pandas as pd
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow





class GsheetPreProcessing:
    
    def __init__(self, base_path):
        self.base_path = base_path
        self.SCOPES = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
    
    def get_gsheet_service(self):
        creds = None
        
        # Load or create credentials
        if os.path.exists(self.base_path + 'token.pickle'):
            with open(self.base_path + 'token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.base_path + 'requirements/client_secret_595891043796-nfhkfrbb8q8gv0oip9vc743k9p64t4gj.apps.googleusercontent.com.json',  # Ensure correct path
                    self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open(self.base_path + 'token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        # Build the service
        service = build('sheets', 'v4', credentials=creds)
        return service
    
    def fetch_sheet_data(self, sample_range_name, sample_spreadsheet_id):
        service = self.get_gsheet_service()
        sheet = service.spreadsheets()
        
        # Get data from the Google Sheet
        result = sheet.values().get(spreadsheetId=sample_spreadsheet_id,
                                    range=sample_range_name).execute()
        values = result.get('values', [])
        
        # Convert to DataFrame
        if not values:
            print('No data found.')
            return None
        else:
            df = pd.DataFrame(values)
            df.columns = df.iloc[0]  # Set the first row as the header
            df = df.drop(df.index[0])  # Drop the first row
            return df

    # def output_to_new_sheet(self, df, sample_spreadsheet_id, new_sheet_name):
    #     service = self.get_gsheet_service()
    #     sheet = service.spreadsheets()
        
    #     df = df.fillna('')

    #     # Fetch the new sheet ID
    #     spreadsheet = service.spreadsheets().get(spreadsheetId=sample_spreadsheet_id).execute()
    #     sheet_id = None
    #     for s in spreadsheet['sheets']:
    #         if s['properties']['title'] == new_sheet_name:
    #             sheet_id = s['properties']['sheetId']
    #             break
        
    #     if sheet_id is None:
    #         print("Error: Could not create or find the new sheet.")
    #         return

    #     # Prepare data to be written
    #     values = [df.columns.values.tolist()] + df.values.tolist()  # Convert DataFrame to list of lists

    #     # Write the data to the new sheet
    #     update_range = f'{new_sheet_name}!A1'
    #     body = {'values': values}
        
    #     sheet.values().update(
    #         spreadsheetId=sample_spreadsheet_id,
    #         range=update_range,
    #         valueInputOption='RAW',
    #         body=body
    #     ).execute()

    #     print(f"Data successfully written to the new worksheet '{new_sheet_name}'.")
