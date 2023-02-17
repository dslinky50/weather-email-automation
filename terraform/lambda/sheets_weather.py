

def lambda_handler(event, context):
    response = {
        'statusCode': 200,
        'body': event
    }
    print(response)
    return(response)