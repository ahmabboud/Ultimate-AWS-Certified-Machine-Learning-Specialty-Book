# Hands-on Lab: Advanced Model Implementation with Amazon SageMaker

In this lab, we'll implement and evaluate advanced modeling techniques using Amazon SageMaker, focusing on ensemble methods and generative AI with Amazon Bedrock. We'll also cover model evaluation and optimization strategies.

## Prerequisites

- An AWS account with SageMaker and Bedrock access
- Familiarity with Python and machine learning concepts
- Basic knowledge of SageMaker and Jupyter notebooks

## Lab Steps

### 1. Environment Setup

1. Open the Amazon SageMaker console at https://console.aws.amazon.com/sagemaker/
2. Create a new SageMaker notebook instance:
   - Choose an instance type (e.g., ml.t3.medium)
   - Set up an IAM role with necessary permissions for SageMaker and Bedrock
   - Launch the instance
3. Open JupyterLab once the instance is ready

### 2. Ensemble Implementation

1. Create a new Jupyter notebook for ensemble methods
2. Import necessary libraries and load a dataset:

```python
import sagemaker
from sagemaker.sklearn.estimator import SKLearn
from sagemaker.xgboost.estimator import XGBoost
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

# Load and split the data
data = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2)

# Convert to DataFrame and save as CSV
train_data = pd.DataFrame(X_train, columns=data.feature_names)
train_data['target'] = y_train
train_data.to_csv('train.csv', index=False, header=False)
```

3. Implement a stacking ensemble with Random Forest and XGBoost:

```python
# Define base models
rf_estimator = SKLearn(
    entry_point='rf_script.py',
    instance_type='ml.m5.large',
    framework_version='0.23-1',
    role=sagemaker.get_execution_role()
)

xgb_estimator = XGBoost(
    entry_point='xgb_script.py',
    instance_type='ml.m5.large',
    framework_version='1.2-1',
    role=sagemaker.get_execution_role()
)

# Train base models
rf_estimator.fit({'train': train_data_location})
xgb_estimator.fit({'train': train_data_location})

# Get predictions from base models
rf_predictions = rf_estimator.predict(X_test)
xgb_predictions = xgb_estimator.predict(X_test)

# Train a meta-model (logistic regression) on the predictions
from sklearn.linear_model import LogisticRegression
meta_features = np.column_stack((rf_predictions, xgb_predictions))
meta_model = LogisticRegression()
meta_model.fit(meta_features, y_test)

# Make final predictions
final_predictions = meta_model.predict(meta_features)
```

### 3. Model Evaluation

1. Implement evaluation metrics:

```python
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

def evaluate_model(y_true, y_pred, y_prob=None):
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    
    if y_prob is not None:
        auc_roc = roc_auc_score(y_true, y_prob)
    else:
        auc_roc = None
    
    return {
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1 Score': f1,
        'AUC-ROC': auc_roc
    }

# Evaluate the ensemble model
ensemble_metrics = evaluate_model(y_test, final_predictions, meta_model.predict_proba(meta_features)[:, 1])
print("Ensemble Model Metrics:", ensemble_metrics)
```

2. Implement cross-validation:

```python
from sklearn.model_selection import cross_val_score

cv_scores = cross_val_score(meta_model, meta_features, y_test, cv=5)
print("Cross-validation scores:", cv_scores)
print("Mean CV score:", cv_scores.mean())
```

### 4. Advanced Optimization

1. Implement hyperparameter tuning for XGBoost:

```python
from sagemaker.tuner import HyperparameterTuner, ContinuousParameter, IntegerParameter

hyperparameter_ranges = {
    'max_depth': IntegerParameter(3, 10),
    'eta': ContinuousParameter(0.01, 0.3),
    'gamma': ContinuousParameter(0, 5),
    'min_child_weight': ContinuousParameter(1, 10),
    'subsample': ContinuousParameter(0.5, 1.0)
}

objective_metric_name = 'validation:auc'

tuner = HyperparameterTuner(
    xgb_estimator,
    objective_metric_name,
    hyperparameter_ranges,
    max_jobs=10,
    max_parallel_jobs=3
)

tuner.fit({'train': train_data_location, 'validation': validation_data_location})

best_model = tuner.best_estimator()
```

### 5. Generative AI with Amazon Bedrock

1. Set up Amazon Bedrock:

```python
import boto3

bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'
)
```

2. Implement text generation using a foundation model:

```python
def generate_text(prompt, max_tokens=100):
    response = bedrock.invoke_model(
        modelId='ai21.j2-ultra-v1',
        contentType='application/json',
        accept='application/json',
        body=json.dumps({
            "prompt": prompt,
            "maxTokens": max_tokens,
            "temperature": 0.7,
            "topP": 1,
            "stopSequences":[],
            "countPenalty":{"scale":0},
            "presencePenalty":{"scale":0},
            "frequencyPenalty":{"scale":0}
        })
    )
    
    response_body = json.loads(response['body'].read())
    return response_body['completions'][0]['data']['text']

# Example usage
generated_text = generate_text("Explain the concept of ensemble learning in machine learning:")
print(generated_text)
```

### 6. Clean Up Resources

1. Delete the SageMaker notebook instance
2. Delete any S3 buckets created during the lab
3. Revoke Bedrock access if no longer needed

## Common Mistakes and Best Practices

- Ensure proper data preprocessing before model training
- Validate model performance using multiple evaluation metrics
- Use cross-validation to get robust performance estimates
- Optimize hyperparameters for better model performance
- Be cautious with generative AI outputs and validate results



