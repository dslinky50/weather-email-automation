import pygsheets
import pandas as pd
import os
import boto3

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
        
    s3_client.download_file('test-google-creds', 'pygsheets.json', '/tmp/pygsheets.json')
    gc = pygsheets.authorize(service_file='/tmp/pygsheets.json')

    # Create empty dataframe
    df = pd.DataFrame()

    # Create a column
    df['name'] = ['John', 'Steve', 'Sarah']

    #open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
    sh = gc.open('Bandon Weather Data')

    #select the first sheet 
    wks = sh[0]

    #update the first sheet with df, starting at cell B2. 
    wks.set_dataframe(df,(1,1))