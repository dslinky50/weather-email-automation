# Standard Imports
import boto3, os, urllib3, json
from boto3.dynamodb.conditions import Key, Attr
from datetime import date, datetime, timedelta
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from mako.template import Template
from decimal import *

###########################
## ENVIRONMENT VARIABLES ##
###########################

weather_api_key = os.environ['WEATHER_API_KEY']
sender_email = 'dylan@big-birdie-tracker.com'
receiver_email = os.environ['EMAIL_LIST']
subject = 'Scotland 2026 Trip/Weather Update'

#####################
## WEATHER SECTION ##
#####################

def get_weather():
    http = urllib3.PoolManager()

    # Today api call
    today_response = json.loads(http.request('GET', f'http://api.weatherapi.com/v1/forecast.json?key={weather_api_key}&q=EH1&days=1&aqi=no&alerts=no').data.decode('utf-8'))
    temp = today_response['forecast']['forecastday'][0]['day']['avgtemp_f']
    wind = today_response['forecast']['forecastday'][0]['day']['maxwind_mph']
    rain_chance = today_response['forecast']['forecastday'][0]['day']['daily_chance_of_rain']
    precip = today_response['forecast']['forecastday'][0]['day']['totalprecip_in']
    condition = today_response['forecast']['forecastday'][0]['day']['condition']['text']

    return temp, wind, rain_chance, precip, condition;

def scotland_date():
    # Scotland count down
    scotland = date(2026, 5, 1)
    today = date.today()
    diff = (scotland - today).days
    return diff

def create_weekly_dates():
    # Weekly date calculator
    week_list = []
    sat = datetime.now()
    fri = sat - timedelta(1)
    thur = sat - timedelta(2)
    wed = sat - timedelta(3)
    tues = sat - timedelta(4)
    mon = sat - timedelta(5)
    sun = sat - timedelta(6)
    sat = sat.strftime('%Y-%m-%d')
    fri = fri.strftime('%Y-%m-%d')
    thur = thur.strftime('%Y-%m-%d')
    wed = wed.strftime('%Y-%m-%d')
    tues = tues.strftime('%Y-%m-%d')
    mon = mon.strftime('%Y-%m-%d')
    sun = sun.strftime('%Y-%m-%d')
    week_list.extend([sun, mon, tues, wed, thur, fri, sat])
    return week_list

######################
## DATABASE SECTION ##
######################

def Average(lst):
    if sum(lst) == 0:
        return 0
    else:
        return sum(lst) / len(lst)

def query_db():
    # Establish DB Connection
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('bandon-weather-data')

    # Use necessary functions
    week_list = create_weekly_dates()

    # Pre-set weekly average lists
    gust_wk_avg = []
    precip_wk_avg = []
    temp_wk_avg = []
    wind_wk_avg = []

    # Query DB
    for date in week_list:
        gust_addr = []
        precip_addr = []
        temp_addr = []
        wind_addr = []
        response = table.scan(
            FilterExpression=Attr('Date').begins_with(date)
        )
        for item in response['Items']:
            gust = item['Gust']
            gust_addr.append(float(gust))
            precip = item['Precipitation']
            precip_addr.append(float(precip))
            temp = item['Temperature']
            temp_addr.append(int(temp))
            wind = item['Wind']
            wind_addr.append(float(wind))

        gust_wk_avg.append(Average(gust_addr))
        precip_wk_avg.append(Average(precip_addr))
        temp_wk_avg.append(Average(temp_addr))
        wind_wk_avg.append(Average(wind_addr))

    return round(Average(gust_wk_avg), 1), round(Average(precip_wk_avg), 1), round(Average(temp_wk_avg), 1), round(Average(wind_wk_avg), 1);

###################
## EMAIL SECTION ##
###################

def create_email_template():
    # Establish necessary variables
    temp, wind, rain_chance, precip, condition = get_weather()
    wk_gust_avg, wk_precip_avg, wk_temp_avg, wk_wind_avg = query_db()
    days = scotland_date()
    
    # Establish s3 Client
    s3_client = boto3.client('s3')
    s3_client.download_file('weather-email-automation', 'email_template.html', '/tmp/email_template.html')
    with open('/tmp/email_template.html', 'r') as f:
        trial = '''\
        {}
        '''.format(f.read())
    
    tmp = Template(trial)
    transformation = tmp.render(days=days, temp=temp, wind=wind, rain_chance=rain_chance, condition=condition, precip=precip, wk_temp_avg=wk_temp_avg, wk_wind_avg=wk_wind_avg, wk_precip_avg=wk_precip_avg, wk_gust_avg=wk_gust_avg)
    
    return transformation

def send_ses_email():
    # Create Email Templace
    template = create_email_template()

    # Set up AWS SES client
    ses_client = boto3.client('ses', region_name='us-east-1')

    # Set up email message
    message = MIMEMultipart('mixed')
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = receiver_email
    html_part = MIMEText(template, 'html')
    message.attach(html_part)

    # Send email
    try:
        response = ses_client.send_raw_email(
            RawMessage={
                'Data': message.as_string(),
            }
        )
        print("Email sent! Message ID:", response['MessageId'])
        return response['MessageId']
    except ClientError as e:
        print("Error sending email:", e.response['Error']['Message'])
        return e.response['Error']['Message']




def lambda_handler(event, context):
    email = send_ses_email()    
    response = {
        'statusCode': 200,
        'body': 'Sent Message ID: {}'.format(email)
    }
    
    print(response)
    return response

##################################################
#               LOCAL TESTING                    #
# lambda_handler(event='event', context='context')
##################################################
# current email list: dylan.silinski@gmail.com, cabrown253@gmail.com, jeremy.c.silinski@gmail.com, tomslinky@icloud.com