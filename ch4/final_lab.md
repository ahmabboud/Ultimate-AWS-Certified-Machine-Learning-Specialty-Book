<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# Chapter 4: Basic Model Training with Amazon SageMaker

---

## Lab: Iris Classification using XGBoost

This lab will guide you through the process of training and deploying a machine learning model using Amazon SageMaker. We'll use the Iris dataset to train an XGBoost classifier.

### Prerequisites

- An AWS account with SageMaker access
- Basic understanding of Python and machine learning concepts
- Familiarity with Jupyter notebooks


### Lab Steps

#### 1. Environment Setup

1. Open the Amazon SageMaker console at https://console.aws.amazon.com/sagemaker/
2. Create a new SageMaker notebook instance:
    - Choose "Notebook instances" from the left navigation pane
    - Click "Create notebook instance"
    - Enter a name for your notebook instance
    - Choose an instance type (e.g., ml.t3.medium)
    - Select "Create a new role" under IAM role
    - Choose "Create role"
    - Click "Create notebook instance"
3. Once the instance status is "InService", click "Open Jupyter" to launch JupyterLab.

#### 2. Data Preparation

In JupyterLab, create a new Jupyter notebook and run the following code:

```python
# Install and import necessary libraries
!pip install pandas numpy scikit-learn
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris

# Load and prepare the Iris dataset
iris = load_iris()
X, y = iris.data, iris.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

train_data = pd.DataFrame(X_train, columns=iris.feature_names)
train_data['target'] = y_train
test_data = pd.DataFrame(X_test, columns=iris.feature_names)
test_data['target'] = y_test

# Save data to CSV files
train_data.to_csv('train.csv', index=False, header=False)
test_data.to_csv('test.csv', index=False, header=False)
```


#### 3. SageMaker Setup

Set up the SageMaker session and role:

```python
import sagemaker
from sagemaker import get_execution_role

role = get_execution_role()
session = sagemaker.Session()

bucket = session.default_bucket()
prefix = 'sagemaker/DEMO-iris'

train_location = session.upload_data('train.csv', bucket=bucket, key_prefix=prefix)
test_location = session.upload_data('test.csv', bucket=bucket, key_prefix=prefix)
```


#### 4. Model Training

Configure the XGBoost algorithm and start the training job:

```python
from sagemaker.amazon.amazon_estimator import get_image_uri

container = get_image_uri(session.boto_region_name, 'xgboost', '1.0-1')

xgb = sagemaker.estimator.Estimator(container,
                                    role, 
                                    instance_count=1, 
                                    instance_type='ml.m4.xlarge',
                                    output_path=f's3://{bucket}/{prefix}/output',
                                    sagemaker_session=session)

xgb.set_hyperparameters(max_depth=5,
                        eta=0.2,
                        gamma=4,
                        min_child_weight=6,
                        subsample=0.8,
                        objective='multi:softprob',
                        num_class=3,
                        num_round=100)

xgb.fit({'train': train_location, 'validation': test_location})
```


#### 5. Model Deployment

Deploy the trained model and make predictions:

```python
xgb_predictor = xgb.deploy(initial_instance_count=1, instance_type='ml.m4.xlarge')

from sagemaker.predictor import csv_serializer, json_deserializer

xgb_predictor.content_type = 'text/csv'
xgb_predictor.serializer = csv_serializer
xgb_predictor.deserializer = json_deserializer

result = xgb_predictor.predict(test_data.iloc[:, :-1].values).decode('utf-8')
predictions = np.fromstring(result[1:-1], sep=',')
predictions = predictions.reshape(-1, 3)
```


#### 6. Evaluate Results

Calculate accuracy:

```python
predicted_labels = np.argmax(predictions, axis=1)
accuracy = (predicted_labels == y_test).mean()
print(f"Model accuracy: {accuracy:.2f}")
```


#### 7. Clean Up Resources

1. Delete the endpoint:
    - Go to the SageMaker console
    - Choose "Inference" > "Endpoints"
    - Select your endpoint
    - Choose "Actions" > "Delete"
2. Delete the notebook instance:
    - Go to the SageMaker console
    - Select "Notebook instances" from the left navigation pane
    - Select your notebook instance
    - Choose "Actions" > "Stop"
    - Once stopped, choose "Actions" > "Delete"
3. Delete other resources:
    - Delete the S3 bucket created for this lab
    - Delete any CloudWatch logs created during the lab

### Common Mistakes and Best Practices

- Ensure your data is in the correct format for the chosen algorithm.
- Always clean up resources after use to avoid unnecessary charges.
- Consider using SageMaker's hyperparameter tuning capabilities for better results.
- Use SageMaker Experiments to track different versions of your model and their performance.
- Ensure your S3 buckets and IAM roles have appropriate permissions set.

By completing this lab, you've gained hands-on experience with the core components of Amazon SageMaker, including data preparation, model training, deployment, and evaluation.

For more detailed information on getting started with SageMaker, including advanced features and best practices, please refer to the following AWS tutorial:

[Build, Train, Deploy, and Monitor a Machine Learning Model with Amazon SageMaker Studio](https://aws.amazon.com/tutorials/build-train-deploy-monitor-machine-learning-model-sagemaker-studio)

<div style="text-align: center">⁂</div>

[^1]: https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/18750853/46c3aae0-0124-488d-9ac3-c55eec1e98e3/Ch4_lab_instructions.docx

