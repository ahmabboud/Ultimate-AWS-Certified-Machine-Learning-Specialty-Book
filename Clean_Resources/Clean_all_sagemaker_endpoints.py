import boto3
from botocore.exceptions import ClientError

# Initialize the SageMaker client
sagemaker_client = boto3.client('sagemaker')

# Function to delete all SageMaker models
def delete_all_models():
    try:
        # List all models
        models = sagemaker_client.list_models()
        for model in models['Models']:
            model_name = model['ModelName']
            print(f"Deleting model: {model_name}")
            sagemaker_client.delete_model(ModelName=model_name)
            print(f"Model {model_name} deleted.")
    except ClientError as e:
        print(f"Error while deleting models: {e}")

# Function to delete all SageMaker endpoints
def delete_all_endpoints():
    try:
        # List all endpoints
        endpoints = sagemaker_client.list_endpoints()
        for endpoint in endpoints['Endpoints']:
            endpoint_name = endpoint['EndpointName']
            print(f"Deleting endpoint: {endpoint_name}")
            sagemaker_client.delete_endpoint(EndpointName=endpoint_name)
            print(f"Endpoint {endpoint_name} deleted.")
    except ClientError as e:
        print(f"Error while deleting endpoints: {e}")

# Function to delete all SageMaker endpoint configurations
def delete_all_endpoint_configs():
    try:
        # List all endpoint configurations
        endpoint_configs = sagemaker_client.list_endpoint_configs()
        for config in endpoint_configs['EndpointConfigs']:
            config_name = config['EndpointConfigName']
            print(f"Deleting endpoint configuration: {config_name}")
            sagemaker_client.delete_endpoint_config(EndpointConfigName=config_name)
            print(f"Endpoint configuration {config_name} deleted.")
    except ClientError as e:
        print(f"Error while deleting endpoint configurations: {e}")

# Clean up all SageMaker resources
def clean_up_sagemaker_resources():
    delete_all_models()
    delete_all_endpoints()
    delete_all_endpoint_configs()

# Call the clean-up function
clean_up_sagemaker_resources()
