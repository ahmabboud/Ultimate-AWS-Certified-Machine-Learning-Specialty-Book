

# **Lab Instructions: Titanic Data Visualization and Bias Evaluation**

This lab will guide you through using Python and Amazon QuickSight to visualize and analyze survival rates from the Titanic dataset. You will explore survival rates based on gender (`gender`) and passenger class (`pclass`) while learning how to evaluate potential biases in the data.

---

## **Lab Objectives**
1. Perform data visualization using Python libraries (`Seaborn`, `Matplotlib`).
2. Create an interactive dashboard in Amazon QuickSight.
3. Evaluate potential bias in survival rates based on gender and passenger class.

---

## **Repository Structure**
Ensure that you have the following files in your repository:

repo: https://github.com/ahmabboud/Ultimate-AWS-Certified-Machine-Learning-Specialty-Book.git

```
ch3/
├── datasets/
│   ├── titanic_filtered.csv       # Filtered Titanic dataset
│   ├── titanic_manifest.json      # Manifest file for QuickSight
├── scripts/
│   ├── Ch3Lab.ipynb               # Jupyter Notebook for this lab
```

---

## **Prerequisites**
1. **AWS Account**: Ensure you have an active AWS account.
2. **IAM Permissions**:
   - Permissions to access Amazon S3 and QuickSight.
   - Ensure QuickSight has access to your S3 bucket (detailed instructions provided below).
3. **Python Environment**:
   - Install the following libraries:
     ```bash
     pip install pandas seaborn matplotlib boto3 pydataset
     ```

---

## **Step 1: Sign Up for Amazon QuickSight**

1. Open the [Amazon QuickSight sign-up page](https://aws.amazon.com/pm/quicksight/).
2. Log in to your AWS account.
3. From the AWS Management Console, search for **QuickSight** under the Analytics section or use the search bar.
4. Click **Sign up for QuickSight**.
5. Choose either the **Standard** or **Enterprise** edition based on your requirements:
   - For most labs, the **Standard Edition** is sufficient.
6. Follow the on-screen instructions to complete the setup.

For detailed steps, refer to [Signing up for Amazon QuickSight](https://docs.aws.amazon.com/quicksight/latest/user/signing-up.html).

---

## **Step 2: Load and Explore the Titanic Dataset**

### **2.1 Load Dataset**
We will use the Titanic dataset from the `pydataset` library.

```python
from pydataset import data
import pandas as pd

# Load Titanic dataset
titanic = data('titanic')

# Preview the dataset
print(titanic.head())
```

### **2.2 Data Preparation**
Rename columns for clarity and convert survival status (`survived`) into a binary format (0 = No, 1 = Yes).

```python
# Rename columns for clarity
titanic.rename(columns={'class': 'pclass', 'age': 'age_group', 'sex': 'gender', 'survived': 'survived_status'}, inplace=True)

# Convert 'survived_status' to binary (0 = No, 1 = Yes)
titanic['survived'] = titanic['survived_status'].apply(lambda x: 1 if x == 'yes' else 0)

# Display summary statistics
print(titanic[['gender', 'pclass', 'survived']].describe())
```

---

## **Step 3: Visualize Data Using Python**

### **3.1 Survival Rates by Gender**
Visualize survival rates based on gender using a bar plot.

```python
import seaborn as sns
import matplotlib.pyplot as plt

# Bar plot for survival rates by gender
sns.countplot(x='survived', hue='gender', data=titanic)
plt.title('Survival Rates by Gender')
plt.xlabel('Survived (0 = No, 1 = Yes)')
plt.ylabel('Count')
plt.legend(title='Gender')
plt.show()
```

### **3.2 Survival Rates by Passenger Class**
Visualize survival rates based on passenger class using a bar plot.

```python
# Bar plot for survival rates by passenger class
sns.countplot(x='survived', hue='pclass', data=titanic)
plt.title('Survival Rates by Passenger Class')
plt.xlabel('Survived (0 = No, 1 = Yes)')
plt.ylabel('Count')
plt.legend(title='Passenger Class')
plt.show()
```

---

## **Step 4: Save Dataset for Amazon QuickSight**

Save the filtered dataset containing only relevant fields (`gender`, `pclass`, and `survived`) as a CSV file under `ch3/datasets/`.

```python
# Save filtered dataset to CSV
titanic_filtered = titanic[['gender', 'pclass', 'survived']]
titanic_filtered.to_csv('ch3/datasets/titanic_filtered.csv', index=False)

print("Filtered dataset saved as 'ch3/datasets/titanic_filtered.csv'.")
```

---

## **Step 5: Configure Permissions in Amazon QuickSight**

### Grant QuickSight Access to S3:
1. Open the **Amazon QuickSight** service in AWS.
2. Click on your account icon (top-right corner) and select **Manage QuickSight**.
3. Go to the **Security & permissions** tab.
4. Under **QuickSight access to AWS services**, click on **Manage** under the IAM role in use.
5. Ensure that **Amazon S3** is selected.
6. Select your S3 bucket (e.g., `titanic-lab-data`).
7. Click **Save**.

---

## **Step 6: Create Visualizations in Amazon QuickSight**

### Connect Dataset:
Use the manifest file located at `ch3/datasets/titanic_manifest.json`. Upload this manifest file to your S3 bucket and connect it in QuickSight:
1. In QuickSight, go to **Datasets** > **New Dataset** > **S3**.
2. Select your manifest file (`titanic_manifest.json`).
3. Preview and save the dataset.

### Create Visualizations:
- Bar Chart: Survival Rates by Gender
  - X-axis: `survived`
  - Group/Color: `gender`
  - Aggregation: Count
- Stacked Bar Chart: Survival Rates by Gender and Passenger Class
  - X-axis: `survived`
  - Group/Color: `gender`
  - Additional Dimension: `pclass`
  - Aggregation: Count

Save your analysis as a dashboard.

---

## **Step 7: Terminate Resources**

### Warning:
To avoid incurring unnecessary costs, ensure that you delete all resources created during this lab after completion.

### Steps to Terminate Resources:
1. Delete datasets from Amazon QuickSight:
   - Go to your profile icon > Manage QuickSight > Datasets.
   - Delete all datasets related to this lab.
2. Delete your S3 bucket:
   - Navigate to S3 in AWS Management Console.
   - Delete the bucket used for this lab (e.g., `titanic-lab-data`).
3. Terminate your QuickSight subscription if no longer needed:
   - Go to your profile icon > Manage QuickSight > Account settings > Account termination.
   - Follow on-screen instructions to delete your account.

For detailed steps, refer to [Deleting Your Amazon QuickSight Subscription](https://docs.aws.amazon.com/en_us/quicksight/latest/user/closing-account.html).

---

This lab provides hands-on experience with visualization techniques, EDA, and bias evaluation—key skills for real-world machine learning workflows and AWS certification exams!

Citations:
- [1] https://aws.amazon.com/pm/quicksight/
- [2] https://docs.aws.amazon.com/quicksight/latest/user/signing-up.html
- [3] https://docs.aws.amazon.com/en_us/quicksight/latest/user/closing-account.html