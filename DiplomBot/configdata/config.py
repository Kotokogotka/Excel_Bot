from __future__ import print_function
import google.auth
import gspread as gspread
from google.oauth2.gdch_credentials import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dataclasses import dataclass
from environs import Env
import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from aiogram import Router
from datetime import datetime

yestoday = datetime.now().day


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм боту


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env("BOT_TOKEN")))


router: Router = Router()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SAMPLE_SPREADSHEET_ID = '1Q9tONyZayA_oAb6uzxt88OdA4Ba9B3FAtyFc3FKub7k'
SAMPLE_RANGE_NAME = 'May!B17:Z39'

def get_google_sheet_api():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                r'C:\Users\asics\Desktop\AtlantBot\configdata\credentials.json',
                SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    return service.spreadsheets()


def get_sheet_data():
    service = get_google_sheet_api()
    result = service.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                  range=SAMPLE_RANGE_NAME).execute()
    return result.get('values', [])


def update_sheet_data(cell, symbol):
    service = get_google_sheet_api()
    values = [[symbol]]
    body = {'values': values}
    range_name = f'May!{cell}'
    service.values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=range_name,
        valueInputOption='RAW',
        body=body).execute()


date_row = ['G11', 'I11', 'K11', 'M11', 'O11', 'Q11', 'S11', 'U11']


def process_sheet_data():
    # Получаем данные из Google Sheets
    data = get_sheet_data()
    cnt = 0
    while cnt < len(data):
        name = name[cnt][0]
        number = input(f'Введите дату заполнения {name}: ')
        for cell in date_row:
            date = data[cnt][1]
            symbol = input(f'Введите символ (+/-/O) для {date}: ')
            update_sheet_data(f'{cell}{number}', symbol)
        cnt += 1


process_sheet_data()
