import boto3
import json
import time

# Initialize the Kinesis client
kinesis_client = boto3.client('kinesis', region_name='us-east-1')

# Define the Kinesis stream name
stream_name = 'StreamingDataPipeline'

# Create sample data
sample_data = [
    {"customer_id": "101", "purchase_amount": 45.67, "timestamp": "2024-12-09T12:00:00Z"},
    {"customer_id": "102", "purchase_amount": 89.23, "timestamp": "2024-12-09T12:01:00Z"},
]

# Send data to the Kinesis stream
for record in sample_data:
    kinesis_client.put_record(
        StreamName=stream_name,
        Data=json.dumps(record),
        PartitionKey=record["customer_id"]
    )
    print(f"Sent record: {record}")
    time.sleep(1)  # Wait 1 second between records
