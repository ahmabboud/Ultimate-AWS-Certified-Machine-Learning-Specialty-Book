
# A/B Testing Deployment with Amazon SageMaker

This document guides you step-by-step on implementing an A/B testing deployment strategy for machine learning models using Amazon SageMaker, including clear explanations of each step.

## Prerequisites
Ensure you have:
- An AWS account with SageMaker access
- Basic knowledge of Python and machine learning

## Lab Overview
In this lab, you'll:
1. Set up the SageMaker environment.
2. Prepare and upload a small dataset.
3. Train two distinct models.
4. Deploy the models with A/B testing.
5. Evaluate performance.
6. Clean up AWS resources.

---

### Step 1: Environment Setup
```python
# Importing necessary libraries for AWS SageMaker interaction and data handling
import boto3
import sagemaker
import pandas as pd
import numpy as np
from sagemaker import get_execution_role

# Setup SageMaker session and execution role
session = sagemaker.Session()
role = get_execution_role()
```

---

### Step 2: Data Preparation and Upload
Using the Iris dataset for simplicity and quick training.

```python
# Loading and splitting the Iris dataset (only first 100 samples for simplicity)
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

iris = load_iris()
X, y = iris.data[:100], iris.target[:100]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Saving the dataset locally
train_data = pd.DataFrame(X_train, columns=iris.feature_names)
train_data['target'] = y_train
train_data.to_csv('train.csv', index=False, header=False)

# Uploading training data to AWS S3 for SageMaker
s3_input_train = session.upload_data(path='train.csv', key_prefix='sagemaker/iris/train')
```

---

### Step 3: Model Training
Training two different models: Random Forest and SVM.

**Random Forest Model:**

```python
%%writefile train_model_a.py
# Script for training a Random Forest model
from sklearn.ensemble import RandomForestClassifier
import argparse, joblib, os
import numpy as np

# Parsing script arguments
parser = argparse.ArgumentParser()
parser.add_argument('--n-estimators', type=int, default=10)
parser.add_argument('--model-dir', type=str, default=os.environ['SM_MODEL_DIR'])
parser.add_argument('--train', type=str, default=os.environ['SM_CHANNEL_TRAIN'])
args, _ = parser.parse_known_args()

# Loading training data
train_data = np.loadtxt(os.path.join(args.train, 'train.csv'), delimiter=',')
X, y = train_data[:, :-1], train_data[:, -1]

# Training model and saving it
model = RandomForestClassifier(n_estimators=args.n_estimators)
model.fit(X, y)
joblib.dump(model, os.path.join(args.model_dir, 'model.joblib'))
```

**SVM Model:**

```python
%%writefile train_model_b.py
# Script for training an SVM model
from sklearn.svm import SVC
import argparse, joblib, os
import numpy as np

# Parsing script arguments
parser = argparse.ArgumentParser()
parser.add_argument('--C', type=float, default=1.0)
parser.add_argument('--model-dir', type=str, default=os.environ['SM_MODEL_DIR'])
parser.add_argument('--train', type=str, default=os.environ['SM_CHANNEL_TRAIN'])
args, _ = parser.parse_known_args()

# Loading training data
train_data = np.loadtxt(os.path.join(args.train, 'train.csv'), delimiter=',')
X, y = train_data[:, :-1], train_data[:, -1]

# Training model and saving it
model = SVC(C=args.C)
model.fit(X, y)
joblib.dump(model, os.path.join(args.model_dir, 'model.joblib'))
```

---

### Step 4: Deploy Models with A/B Testing
Deploying both models simultaneously for A/B testing on SageMaker.

```python
from sagemaker.session import production_variant
from sagemaker.serializers import CSVSerializer
from sagemaker.deserializers import JSONDeserializer
from datetime import datetime

# Creating model objects from trained estimators
model_a = sklearn_estimator_a.create_model()
model_b = sklearn_estimator_b.create_model()

# Explicitly registering models in SageMaker
timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
model_a.name = f"model-a-{timestamp}"
model_b.name = f"model-b-{timestamp}"

model_a._create_sagemaker_model(instance_type='ml.c4.2xlarge', accelerator_type=None)
model_b._create_sagemaker_model(instance_type='ml.c4.2xlarge', accelerator_type=None)

# Defining variants for A/B testing deployment
variant1 = production_variant(model_name=model_a.name, instance_type="ml.c4.2xlarge",
                              initial_instance_count=1, variant_name='ModelA', initial_weight=50)
variant2 = production_variant(model_name=model_b.name, instance_type="ml.c4.2xlarge",
                              initial_instance_count=1, variant_name='ModelB', initial_weight=50)

endpoint_name = 'iris-ab-test-endpoint'

# Deploying endpoint with two production variants (A/B testing)
session.endpoint_from_production_variants(name=endpoint_name, production_variants=[variant1, variant2])

# Predictor setup to test deployed endpoint
predictor = sagemaker.Predictor(endpoint_name=endpoint_name, sagemaker_session=session,
                                serializer=CSVSerializer(), deserializer=JSONDeserializer())
```

---

### Step 5: Evaluate Performance
You should include a script here to send data to your endpoint and measure the performance and variant distribution.

---

### Step 6: Clean Up AWS Resources
Always delete resources to avoid additional AWS charges.

```python
# Delete endpoint and resources after testing
session.delete_endpoint(endpoint_name='iris-ab-test-endpoint')

# Delete endpoint configuration
sm_client = boto3.client('sagemaker')
sm_client.delete_endpoint_config(EndpointConfigName='iris-ab-test-endpoint')

# Delete models explicitly
sm_client.delete_model(ModelName=model_a.name)
sm_client.delete_model(ModelName=model_b.name)
```

---

## Conclusion
You've successfully implemented an A/B testing deployment with Amazon SageMaker, including resource cleanup to prevent unnecessary charges.

**Best Practices:**
- Always monitor AWS resource usage.
- Keep models and endpoint names unique to avoid conflicts.
- Clean up resources immediately after use to minimize costs.
