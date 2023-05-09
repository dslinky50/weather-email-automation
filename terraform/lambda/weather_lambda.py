import boto3, os, urllib3, json
from boto3.dynamodb.conditions import Key, Attr
from decimal import *

###########################
## ENVIRONMENT VARIABLES ##
###########################

weather_api_key = os.environ['WEATHER_API_KEY']

#####################
## WEATHER SECTION ##
#####################

def get_weather():
    http = urllib3.PoolManager()

    # Today api call
    today_response = json.loads(http.request('GET', f'http://api.weatherapi.com/v1/forecast.json?key={weather_api_key}&q=97411&days=1&aqi=no&alerts=no').data.decode('utf-8'))
    temp = today_response['current']['temp_f']
    wind = today_response['current']['wind_mph']
    gust = today_response['current']['gust_mph']
    precip = today_response['current']['precip_in']
    today = today_response['current']['last_updated']
    return gust, precip, temp, today, wind
#get_weather()

######################
## DATABASE SECTION ##
######################

def put_in_db():
    # Establish DB Connection
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('bandon-weather-data')

    # Weather API Call
    gust, precip, temp, today, wind = get_weather()

    # Build Data Input
    data_input = {}
    data_input['Date'] = today
    data_input['Gust'] = format(Decimal(gust), '.2g')
    data_input['Precipitation'] = format(Decimal(precip), '.2g')
    data_input['Temperature'] = format(Decimal(temp), '.2g')
    data_input['Wind'] = format(Decimal(wind), '.2g')

    # Input Data
    table.put_item(Item=data_input)
    return data_input

def lambda_handler(event, context):
    input = put_in_db()    
    response = {
        'statusCode': 200,
        'body': input
    }
    
    print(response)
    return response