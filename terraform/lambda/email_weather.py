# Standard Imports
import boto3, os, urllib3, json
from datetime import date, datetime, timedelta
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from mako.template import Template

###########################
## ENVIRONMENT VARIABLES ##
###########################

weather_api_key = os.environ['WEATHER_API_KEY']
sender_email = 'dylan@big-birdie-tracker.com'
receiver_email = os.environ['EMAIL_LIST']
subject = 'Bandon 2024 Trip/Weather Update'

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

    # Weekly
    wk_temp_count = 0
    wk_wind_count = 0
    wk_precip_count = 0
    week_list = create_weekly_dates()
    for date in week_list:
        response = json.loads(http.request('GET', f'http://api.weatherapi.com/v1/history.json?key={weather_api_key}&q=97411&dt={date}').data.decode('utf-8'))
        for day in response['forecast']['forecastday']:
            temp = day['day']['avgtemp_f']
            wind = day['day']['maxwind_mph']
            precip = day['day']['totalprecip_in']
            wk_temp_count += temp
            wk_wind_count += wind
            wk_precip_count += precip
    wk_temp_avg = round(wk_temp_count/7, 1)
    wk_wind_avg = round(wk_wind_count/7, 1)
    wk_precip_avg = round(wk_precip_count/7, 1)

    return temp, wind, gust, precip, wk_temp_avg, wk_wind_avg, wk_precip_avg;

def bandon_date():
    # Bandon count down
    bandon = date(2024, 11, 1)
    today = date.today()
    diff = (bandon - today).days
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

###################
## EMAIL SECTION ##
###################

def create_email_template():
    # Establish necessary variables
    temp, wind, gust, precip, wk_temp_avg, wk_wind_avg, wk_precip_avg = get_weather()
    days = bandon_date()
    
    # Establish s3 Client
    s3_client = boto3.client('s3')
    s3_client.download_file('weather-email-automation', 'email_template.html', '/tmp/email_template.html')
    with open('/tmp/email_template.html', 'r') as f:
        trial = '''\
        {}
        '''.format(f.read())
    
    tmp = Template(trial)
    transformation = tmp.render(days=days, temp=temp, wind=wind, gust=gust, precip=precip, wk_temp_avg=wk_temp_avg, wk_wind_avg=wk_wind_avg, wk_precip_avg=wk_precip_avg)
    
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
lambda_handler(event='event', context='context')
##################################################
# current email list: dylan.silinski@gmail.com, cabrown253@gmail.com, jeremy.c.silinski@gmail.com, tomslinky@icloud.com