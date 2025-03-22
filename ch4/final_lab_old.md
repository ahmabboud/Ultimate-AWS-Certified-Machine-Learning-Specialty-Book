<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# Chapter 4: Basic Model Training with Amazon SageMaker

---

## Lab: Iris Classification using XGBoost

This lab guides you through the process of training and deploying a machine learning model using Amazon SageMaker. We'll use the Iris dataset to train an XGBoost classifier.

### Prerequisites

- An AWS account with SageMaker access
- Familiarity with Python and basic machine learning concepts


### Step 1: Set up the SageMaker environment

```python
# Import necessary libraries
import sagemaker
import boto3
from sagemaker.session import Session
from sagemaker import get_execution_role

# Initialize the SageMaker session
session = sagemaker.Session()

# Get the SageMaker execution role
role = get_execution_role()

# Print the role ARN for verification
print(f"SageMaker Execution Role: {role}")
```

This step initializes the SageMaker session and retrieves the execution role. The role is crucial for granting necessary permissions to SageMaker for accessing AWS resources.

### Step 2: Prepare the dataset

```python
# Import libraries for data manipulation and machine learning
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# Load the Iris dataset
iris = load_iris()
X, y = iris.data, iris.target

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create DataFrames for training and testing data
train_data = pd.DataFrame(X_train, columns=iris.feature_names)
train_data['target'] = y_train
test_data = pd.DataFrame(X_test, columns=iris.feature_names)
test_data['target'] = y_test

# Save the data to CSV files
train_data.to_csv('train.csv', index=False, header=False)
test_data.to_csv('test.csv', index=False, header=False)
```

Here, we load the Iris dataset, split it into training and testing sets, and save them as CSV files. This prepares our data for use with SageMaker.

### Step 3: Upload data to S3

```python
# Upload the training and testing data to S3
bucket = session.default_bucket()  # Use the default SageMaker bucket
prefix = 'sagemaker/DEMO-xgboost-iris'

# Upload training and testing data to S3
train_location = session.upload_data('train.csv', bucket=bucket, key_prefix=prefix)
test_location = session.upload_data('test.csv', bucket=bucket, key_prefix=prefix)

print(f"Training data uploaded to: {train_location}")
print(f"Testing data uploaded to: {test_location}")
```

This step uploads our prepared datasets to an S3 bucket. SageMaker will access the data from this location during training.

### Step 4: Define the XGBoost model

```python
# Import the XGBoost estimator from SageMaker
from sagemaker.xgboost.estimator import XGBoost

# Define the XGBoost model
xgb_model = XGBoost(entry_point='xgboost_script.py',
                    framework_version='1.5-1',
                    instance_type='ml.m5.xlarge',
                    instance_count=1,
                    role=role,
                    output_path=f's3://{bucket}/{prefix}/output',
                    hyperparameters={
                        'max_depth': 5,
                        'eta': 0.2,
                        'gamma': 4,
                        'min_child_weight': 6,
                        'subsample': 0.8,
                        'objective': 'multi:softprob',
                        'num_class': 3,
                        'num_round': 100
                    })
```

Here, we define our XGBoost model using SageMaker's XGBoost estimator. We specify the entry point script, instance type, and hyperparameters for our model.

### Step 5: Train the model

```python
# Train the XGBoost model
xgb_model.fit({'train': train_location, 'validation': test_location})
```

This command starts the training job on SageMaker using the specified data locations.

### Step 6: Deploy the model

```python
# Deploy the trained model
xgb_predictor = xgb_model.deploy(initial_instance_count=1, instance_type='ml.t2.medium')
```

After training, we deploy the model to a SageMaker endpoint for making predictions.

### Step 7: Make predictions

```python
# Prepare test data for prediction
test_data_array = test_data.drop('target', axis=1).values.astype('float32')

# Make predictions
predictions = xgb_predictor.predict(test_data_array)

# Process predictions
predicted_labels = np.argmax(predictions, axis=1)
```

Here, we use our deployed model to make predictions on the test data.

### Step 8: Evaluate the model

```python
# Calculate and print the accuracy
accuracy = (predicted_labels == y_test).mean()
print(f"Model accuracy: {accuracy:.2f}")
```

We evaluate our model's performance by calculating its accuracy on the test set.

### Step 9: Clean up resources

```python
# Delete the endpoint to avoid incurring charges
xgb_predictor.delete_endpoint()
print("Endpoint deleted successfully.")
```

Finally, we delete the deployed endpoint to avoid unnecessary charges.

### Conclusion

This lab demonstrated the end-to-end process of training and deploying a machine learning model using Amazon SageMaker. From data preparation to model evaluation, you've experienced the key steps in a typical machine learning workflow on AWS.

For more detailed information on getting started with SageMaker, including advanced features and best practices, please refer to the following AWS tutorial:

[Build, Train, Deploy, and Monitor a Machine Learning Model with Amazon SageMaker Studio](https://aws.amazon.com/tutorials/build-train-deploy-monitor-machine-learning-model-sagemaker-studio)

This comprehensive guide will provide you with further insights into leveraging SageMaker's capabilities for your machine learning projects.

