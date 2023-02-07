# Standard imports
import base64, json, os, urllib3
from datetime import date

# Parsing imports
import httplib2
import html2text
from mako.template import Template
import boto3

# Gmail Modules
from googleapiclient import errors, discovery
from oauth2client import client, tools, file

# Email Modules
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase

def grab_s3_file():
    s3_client = boto3.client('s3')
    
    s3_client.download_file('email-html-bucket-test', 'email_template.html', '/tmp/email_template.html')
    with open('/tmp/email_template.html', 'r') as f:
        trial = '''\
        {}
        '''.format(f.read())
    
    tmp = Template(trial)
    transformation = tmp.render(days=days, temp=temp, wind=wind, gust=gust)
    
    return transformation

###################
## EMAIL SECTION ##
###################

# Email variables. Modify this!
SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'client_secret.json'

def get_credentials():
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']
    refresh_token = os.environ['REFRESH_TOKEN']
    credentials = client.GoogleCredentials(None, client_id, client_secret,refresh_token,None,'https://accounts.google.com/o/oauth2/token','my-user-agent')
    return credentials

def SendMessage(sender, to, subject, msgHtml, msgPlain):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    message1 = CreateMessageHtml(sender, to, subject, msgHtml, msgPlain)
    result = SendMessageInternal(service, 'me', message1)
    return result

def SendMessageInternal(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return 'Error'
    return 'OK'

def CreateMessageHtml(sender, to, subject, msgHtml, msgPlain):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['BCC'] = to
    msg.attach(MIMEText(msgPlain, 'plain'))
    msg.attach(MIMEText(msgHtml, 'html'))
    return {'raw': base64.urlsafe_b64encode(msg.as_string().encode('UTF-8')).decode('ascii')}



def html_to_plain_text(html):
    plain = html2text.html2text(html)
    return plain
    
sender_email = 'dylan.silinski@gmail.com'
receiver_email = os.environ['EMAIL_LIST']
subject = 'Bandon 2024 Trip/Weather Update'


def main(html_file):
    message = SendMessage(sender_email, receiver_email, subject, msgHtml=html_file, msgPlain=html_to_plain_text(html_file))
    return message

#####################
## WEATHER SECTION ##
#####################

weather_api_key = os.environ['WEATHER_API_KEY']

def get_weather():
    http = urllib3.PoolManager()
    response = json.loads(http.request('GET', f'http://api.weatherapi.com/v1/forecast.json?key={weather_api_key}&q=97411&days=7&aqi=no&alerts=no').data.decode('utf-8'))

    temp = response['current']['temp_f']
    wind = response['current']['wind_mph']
    gust = response['current']['gust_mph']
    return temp, wind, gust;

def calc_date():
    bandon = date(2024, 11, 1)
    today = date.today()
    diff = (bandon - today).days
    return diff

temp, wind, gust = get_weather()
days = calc_date()

def lambda_handler(event, context):
    temp, wind, gust = get_weather()
    days = calc_date()
    transformation = grab_s3_file()
    message = main(transformation)    
    response = {
        'statusCode': 200,
        'body': 'Sent Message ID: {}'.format(message['id'])
    }
    
    print(response)
    return response

##################################################
#               LOCAL TESTING                    #
# lambda_handler(event='event', context='context')
##################################################