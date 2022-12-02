import json
import boto3
import re
s3_client = boto3.client('s3')
S3_BUCKET = "hashtablesfk7"
object_key = "data.csv"  


def lambda_handler(event, context):
	try:	
		myHash = event['pathParameters']['shaHash']
		s3_response = s3_client.select_object_content(Bucket='hashtablesfk7', Key='data.csv', ExpressionType='SQL', Expression=f"SELECT s.password FROM s3object s WHERE s.shaHash = '{myHash}'", InputSerialization = {'CSV': {"FileHeaderInfo": "Use"}, 'CompressionType': 'NONE'}, OutputSerialization = {'CSV': {}})
		for event in s3_response["Payload"]:
			if 'Records' in event:
				records = event['Records']['Payload'].decode('utf-8')
				length = len(records)
				passWord = records[0:length-2]
				return{
		    		'statusCode': 200,
		    		'body': 
		    			json.dumps({myHash:passWord})
		    		}
			else:
				return{
					'statusCode': 404,
					'body': json.dumps('Hash not found!')
		        }
	except:
			return{
				'statusCode': 404,
				'body': json.dumps('Hash not found!')
		        }