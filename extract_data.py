import requests
import json
import pandas as pd
import numpy as np
from datetime import datetime


def request_api():
    base_url = 'https://coronavirus.m.pipedream.net/'
    response = requests.request("GET", base_url)
    if response.status_code == 200:
        data = json.loads(response.content)
        raw_data = data['rawData']
        df = pd.DataFrame(raw_data)
        return df
    else:
        return response


def save_data(df):
    today = datetime.now().date()
    df.to_csv(f'./data/data_covid_{today}')


def preprocess_data(df):
    # DATE COLUMNS
    df['Last_Update'] = pd.to_datetime(df['Last_Update'], format='%Y-%m-%d %H:%M:%S')
    # FLOAT COLUMNS
    df.loc[:, ['Lat', 'Long_', 'Incident_Rate',
               'Case_Fatality_Ratio']] = df.loc[:, ['Lat', 'Long_', 'Incident_Rate',
                                                'Case_Fatality_Ratio']].replace('', np.nan)
    df.loc[:, ['Lat', 'Long_', 'Incident_Rate',
               'Case_Fatality_Ratio']] = df.loc[:, ['Lat', 'Long_', 'Incident_Rate',
                                                'Case_Fatality_Ratio']].astype('float')
    # INT COLUMNS
    df.loc[:, ['Confirmed', 'Deaths']] = df.loc[:, ['Confirmed', 'Deaths']].astype('int')

    # SELECT COLUMNS
    df['Long'] = df['Long_']
    df = df.loc[:, ['FIPS', 'Admin2', 'Province_State', 'Country_Region', 'Last_Update', 'Lat',
                'Long', 'Confirmed', 'Deaths', 'Combined_Key', 'Incident_Rate', 'Case_Fatality_Ratio']]
    return df


def extract_and_save():
    df = request_api()
    try:
        df = preprocess_data(df)
        save_data(df)
        return df
    except Exception as e:
        print(e)
        print(df.status)
        return df
