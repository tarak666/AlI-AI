import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import boto3
from botocore.exceptions import ClientError
from config.settings import settings

def create_table():
    dynamodb = boto3.client(
        "dynamodb",
        region_name=settings.AWS_REGION
    )

    try:
        dynamodb.create_table(
            TableName=settings.DDB_TABLE_NAME,
            BillingMode="PAY_PER_REQUEST",
            AttributeDefinitions=[
                {"AttributeName": "incident_id", "AttributeType": "S"}
            ],
            KeySchema=[
                {"AttributeName": "incident_id", "KeyType": "HASH"}
            ]
        )
        print(f"✅ DynamoDB table creation started: {settings.DDB_TABLE_NAME}")

    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceInUseException":
            print(f"ℹ️ DynamoDB table already exists: {settings.DDB_TABLE_NAME}")
        else:
            raise

if __name__ == "__main__":
    create_table()
