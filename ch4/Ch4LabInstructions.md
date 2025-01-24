# Hands-on Lab: Basic Model Training with Amazon SageMaker

This lab will guide you through building and training a machine learning model using Amazon SageMaker. We'll focus on a simple classification problem to demonstrate the core concepts of SageMaker, including environment setup, data preparation, model training, and result analysis.

## Prerequisites

*   An AWS account with SageMaker access
*   Basic understanding of Python and machine learning concepts
*   Familiarity with Jupyter notebooks

## Lab Steps

### 1\. Environment Setup

1.  Open the Amazon SageMaker console at https://console.aws.amazon.com/sagemaker/
2.  Create a new SageMaker notebook instance:
    *   Choose "Notebook instances" from the left navigation pane
    *   Click "Create notebook instance"
    *   Enter a name for your notebook instance
    *   Choose an instance type (e.g., ml.t3.medium)
    *   Select "Create a new role" under IAM role
    *   Choose "Create role"
    *   Click "Create notebook instance"
3.  Once the instance status is "InService", click "Open Jupyter" to launch JupyterLab.

### 2\. Data Preparation

1.  In JupyterLab, create a new Jupyter notebook.
2.  Install and import necessary libraries:

```python
!pip install pandas numpy scikit-learn
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
```

1.  Load and prepare the Iris dataset:

```python
iris = load_iris()
X, y = iris.data, iris.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

train_data = pd.DataFrame(X_train, columns=iris.feature_names)
train_data['target'] = y_train
test_data = pd.DataFrame(X_test, columns=iris.feature_names)
test_data['target'] = y_test

train_data.to_csv('train.csv', index=False, header=False)
test_data.to_csv('test.csv', index=False, header=False)
```

### 3\. SageMaker Setup

Set up SageMaker session and role:

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

### 4\. Model Training

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

### 5\. Model Deployment

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

### 6\. Evaluate Results

Calculate accuracy:

```python
predicted_labels = np.argmax(predictions, axis=1)
accuracy = (predicted_labels == y_test).mean()
print(f"Model accuracy: {accuracy:.2f}")
```

### 7\. Clean Up Resources

Delete the endpoint:

*   Go to the SageMaker console
*   Choose "Inference" > "Endpoints"
*   Select your endpoint
*   Choose "Actions" > "Delete"

Delete the notebook instance:

*   Go to the SageMaker console
*   Select "Notebook instances" from the left navigation pane
*   Select your notebook instance
*   Choose "Actions" > "Stop"
*   Once stopped, choose "Actions" > "Delete"

Delete other resources:

*   Delete the S3 bucket created for this lab
*   Delete any CloudWatch logs created during the lab

## Common Mistakes and Best Practices

*   Ensure your data is in the correct format for the chosen algorithm.
*   Always clean up resources after use to avoid unnecessary charges.
*   Consider using SageMaker's hyperparameter tuning capabilities for better results.
*   Use SageMaker Experiments to track different versions of your model and their performance.
*   Ensure your S3 buckets and IAM roles have appropriate permissions set.

By completing this lab, you've gained hands-on experience with the core components of Amazon SageMaker, including data preparation, model training, deployment, and evaluation.

# Citations:

\[1\] [https://docs.aws.amazon.com/sagemaker/latest/dg/gs-setup-working-env.html?trk=gs_card](https://docs.aws.amazon.com/sagemaker/latest/dg/gs-setup-working-env.html?trk=gs_card)

\[2\] [https://docs.aws.amazon.com/sagemaker/latest/dg/serverless-endpoints-delete.html](https://docs.aws.amazon.com/sagemaker/latest/dg/serverless-endpoints-delete.html)

\[3\] [https://docs.aws.amazon.com/sagemaker/latest/dg/realtime-endpoints-deploy-models.html](https://docs.aws.amazon.com/sagemaker/latest/dg/realtime-endpoints-deploy-models.html)

\[4\] [https://docs.aws.amazon.com/sagemaker/latest/dg/ex1-cleanup.html](https://docs.aws.amazon.com/sagemaker/latest/dg/ex1-cleanup.html)

\[5\] [https://docs.aws.amazon.com/sagemaker/latest/dg/realtime-endpoints-delete-resources.html](https://docs.aws.amazon.com/sagemaker/latest/dg/realtime-endpoints-delete-resources.html)

\[6\] [https://docs.aws.amazon.com/sagemaker/latest/dg/rstudio-byoi-sdk-cleanup.html](https://docs.aws.amazon.com/sagemaker/latest/dg/rstudio-byoi-sdk-cleanup.html)

\[7\] [https://docs.aws.amazon.com/en_jp/sagemaker/latest/dg/howitworks-create-ws.html](https://docs.aws.amazon.com/en_jp/sagemaker/latest/dg/howitworks-create-ws.html)

\[8\] [https://docs.aws.amazon.com/ja_jp/sagemaker/latest/APIReference/API_DeleteEndpoint.html](https://docs.aws.amazon.com/ja_jp/sagemaker/latest/APIReference/API_DeleteEndpoint.html)

\[9\] [https://docs.aws.amazon.com/en_en/sagemaker/latest/dg/canvas-deploy-model.html](https://docs.aws.amazon.com/en_en/sagemaker/latest/dg/canvas-deploy-model.html)

\[10\] [https://docs.aws.amazon.com/en_kr/sagemaker/latest/dg/studio-updated-running-stop.html](https://docs.aws.amazon.com/en_kr/sagemaker/latest/dg/studio-updated-running-stop.html)

\[11\] [https://docs.aws.amazon.com/fr_fr/deepcomposer/latest/devguide/deepcomposer-launch-sagemaker.html](https://docs.aws.amazon.com/fr_fr/deepcomposer/latest/devguide/deepcomposer-launch-sagemaker.html)

\[12\] [https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry-deploy.html](https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry-deploy.html)

\[13\] [https://docs.aws.amazon.com/sagemaker/latest/dg/async-inference-delete-endpoint.html](https://docs.aws.amazon.com/sagemaker/latest/dg/async-inference-delete-endpoint.html)

\[14\] [https://docs.aws.amazon.com/en_kr/sagemaker/latest/dg/jumpstart-deploy.html](https://docs.aws.amazon.com/en_kr/sagemaker/latest/dg/jumpstart-deploy.html)

\[15\] [https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateNotebookInstance.html](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateNotebookInstance.html)

\[16\] [https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html)