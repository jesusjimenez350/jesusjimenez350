import os
import json

from todos import decimalencoder
import boto3

dynamodb = boto3.resource('dynamodb')
translate = boto3.client('translate')


def get(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    
    langToTranslate = event['pathParameters']['lang']
    
    textToTranslate = result['Item']['text']
    
    text_translated = translate.translate_text(Text = textToTranslate, SourceLanguageCode = "auto", TargetLanguageCode = langToTranslate)
    result['Item']['text'] = text_translated['TranslatedText']
    
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response