import csv
import boto3
import json

def lambda_handler(event, context):
    TABLE_NAME = 'bandon-weather-data'
    OUTPUT_BUCKET = 'test-google-creds'
    TEMP_FILENAME = '/tmp/weather.csv'
    OUTPUT_KEY = 'weather.csv'

    s3_resource = boto3.resource('s3')
    dynamodb_resource = boto3.resource('dynamodb')
    table = dynamodb_resource.Table(TABLE_NAME)

    with open(TEMP_FILENAME, 'w') as output_file:
        writer = csv.writer(output_file)
        header = True
        first_page = True

        # Paginate results
        while True:

            # Scan DynamoDB table
            if first_page:
                response = table.scan()
                first_page = False
            else:
                response = table.scan(ExclusiveStartKey = response['LastEvaluatedKey'])

            for item in response['Items']:

                # Write header row?
                if header:
                    writer.writerow(item.keys())
                    header = False

                writer.writerow(item.values())

            # Last page?
            if 'LastEvaluatedKey' not in response:
                break

    # Upload temp file to S3
    s3_resource.Bucket(OUTPUT_BUCKET).upload_file(TEMP_FILENAME, OUTPUT_KEY)

lambda_handler(event='event', context='context')