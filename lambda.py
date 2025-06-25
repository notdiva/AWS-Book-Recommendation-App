'''import boto3
import json
import csv
import io

campaign_arn = 'arn:aws:personalize:ap-southeast-2:436410794863:campaign/test-campaign'
s3_bucket = 'recommend-books'
s3_key = 'book_data.csv'

personalize_runtime = boto3.client('personalize-runtime')
s3_client = boto3.client('s3')

def load_book_titles():
    response = s3_client.get_object(Bucket=s3_bucket, Key=s3_key)
    lines = response['Body'].read().decode('utf-8').splitlines()
    reader = csv.DictReader(lines)
    return {row['item_id']: row['book_title'] for row in reader}

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        user_id = body.get('user_id', 'default-user-id')
    except Exception as e:
        return {
            'statusCode': 400,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token"
            },
            'body': json.dumps({'error': f'Invalid request format: {str(e)}'})
        }

    try:
        response = personalize_runtime.get_recommendations(
            campaignArn=campaign_arn,
            userId=str(user_id)
        )
        item_ids = [item['itemId'] for item in response['itemList']]
        book_titles = load_book_titles()
        recommended_books = [
            {'item_id': item_id, 'title': book_titles.get(item_id, 'Title Not Found')}
            for item_id in item_ids
        ]

        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token"
            },
            'body': json.dumps({'recommended_books': recommended_books})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token"
            },
            'body': json.dumps({'error': f'Failed to fetch recommendations: {str(e)}'})
        }'''
