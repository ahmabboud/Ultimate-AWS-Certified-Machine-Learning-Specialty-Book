
# **Chapter 2: Building an End-to-End Data Pipeline**

Welcome to Chapter 2 of the **Ultimate AWS Certified Machine Learning Specialty MLS-C01 Exam Guide**! In this chapter, you’ll build an **end-to-end data pipeline** using AWS services to ingest, process, and store data.

This README provides all the information you need to run the labs and use the provided scripts and datasets.

---

## **Folder Structure**

The Chapter 2 folder contains the following:

```
ch2/
├── datasets/            # Datasets required for the labs
├── scripts/             # Python scripts for data pipeline workflows
└── README.md            # This file
```

- **datasets/**: Contains sample data files for ingestion into the pipeline.
- **scripts/**: Contains Python scripts to programmatically interact with AWS services.

---

## **Prerequisites**

Before starting this chapter, ensure the following steps are completed:

1. **AWS Account**: You must have an AWS account with sufficient permissions to create and manage resources like S3, Glue, and Kinesis.
2. **Environment Setup**: The Python virtual environment for the repository should already be set up according to the general **repository README**.
3. **AWS Toolkit**: AWS Toolkit should be installed and configured in **Visual Studio Code**, and your AWS credentials should be correctly set up.

If you haven’t completed the general repository setup yet, refer to the [general repository README](../README.md) for step-by-step instructions.

---

## **Objective**

This lab focuses on building a data pipeline that does the following:
1. **Data Ingestion**: Streams data into **Amazon Kinesis**.
2. **Data Processing**: Transforms data using **AWS Glue**.
3. **Data Storage**: Stores the data in **Amazon S3**.

---

## **AWS Services Used**

In this lab, you’ll work with the following AWS services:
1. **Amazon S3**: To store raw and processed data.
2. **Amazon Kinesis**: To ingest and process streaming data.
3. **AWS Glue**: To create ETL (Extract, Transform, Load) jobs for data transformation.

---

## **Step-by-Step Lab**

### **Step 1: Activate the Virtual Environment**

From the **root directory of the repository**, activate the Python virtual environment that you set up during the general repository setup:

- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```
- On Windows:
  ```cmd
  venv\Scripts\activate
  ```

---

### **Step 2: Prepare AWS Resources**

Before running the scripts, you need to create the following AWS resources. You can create these using the AWS Management Console or AWS CLI:

1. **S3 Bucket**:
   - Create an S3 bucket to store raw and processed data.
   - Example bucket name: `ch2-data-pipeline-bucket`.

2. **Kinesis Data Stream**:
   - Create a Kinesis Data Stream to ingest data (on-demmand or provisioned).
   - Example stream name: `ch2-data-pipeline-stream`.
   - Set the number of shards to `1` for simplicity.

3. **AWS Glue Jobs**:
   - Create a Glue job to process and transform data stored in S3.
   - Use the Glue job in one of the provided scripts.

---

### **Step 3: Run the Python Scripts**

Navigate to the `ch2/scripts/` directory to run the Python scripts for this lab. Below are the key scripts and their purposes:

---

#### **Script 1: Sending Data to Kinesis**

**File**: `scripts/send_data_to_kinesis.py`

This script uses the **boto3** library to send streaming data to the Kinesis Data Stream.

1. Open the script in your IDE.
2. Update the **Kinesis Data Stream name** in the script to match the one you created in Step 2.
3. Run the script:
   ```bash
   python scripts/send_data_to_kinesis.py
   ```
4. Verify the data ingestion in the AWS Management Console under **Kinesis > Data Streams**.

---

#### **Script 2: Processing Data with AWS Glue**

**File**: `scripts/process_data_with_glue.py`

This script programmatically creates an AWS Glue job, submits it, and monitors its execution. The Glue job will process raw data from S3 and store the transformed data in another S3 location.

1. Open the script in your IDE.
2. Update the following in the script:
   - The **S3 bucket name** where the raw data is stored.
   - The **S3 destination bucket** for transformed data.
   - The **Glue job name**.
3. Run the script:
   ```bash
   python scripts/process_data_with_glue.py
   ```
4. Monitor the Glue job execution in the AWS Management Console under **AWS Glue > Jobs**.

---

#### **Script 3: Reading Processed Data**

**File**: `scripts/read_processed_data.py`

This script reads the processed data stored in S3 and displays it in the terminal.

1. Open the script in your IDE.
2. Update the **S3 bucket name** and file path in the script.
3. Run the script:
   ```bash
   python scripts/read_processed_data.py
   ```
4. Confirm the processed data output matches the expected results.

---

### **Step 4: Validate the Results**

After running the scripts, validate the following:
1. **Kinesis Data Stream**:
   - Check the AWS Management Console to ensure data was successfully ingested into the Kinesis stream.

2. **S3 Bucket**:
   - Verify that raw data is stored in the S3 source bucket.
   - Confirm that processed data is correctly stored in the destination bucket.

3. **AWS Glue**:
   - Check the Glue job logs in the AWS Management Console to ensure the job ran successfully.

---

### **Step 5: Clean Up Resources**

To avoid incurring unnecessary AWS costs, delete the resources created during this lab:

1. Delete the **S3 buckets** and any objects inside them.
2. Delete the **Kinesis Data Stream**.
3. Delete the **AWS Glue job**.

You can clean up manually in the AWS Management Console or automate the cleanup process using Python or the AWS CLI.

---

## **Datasets**

The `datasets/` folder contains sample data files for this lab. These files will be used to simulate real-world data ingestion. For example:
- **`input_data.json`**: A JSON file with sample records to send to the Kinesis Data Stream.

---

## **Troubleshooting**

### **AWS Credential Errors**
- Ensure your AWS credentials are configured correctly in the AWS Toolkit or `~/.aws/credentials`.
- Verify your IAM user has the necessary permissions (e.g., `AmazonKinesisFullAccess`, `AWSGlueServiceRole`, and `AmazonS3FullAccess`).

### **Script Errors**
- Double-check the resource names (e.g., Kinesis stream, S3 bucket) in the scripts.
- Review the logs in the AWS Management Console for Glue or Kinesis to debug issues.

---

## **Next Steps**

Once you’ve successfully completed the labs for Chapter 2:
- Move on to Chapter 3 to explore **data processing and feature engineering**.
- Experiment with the scripts by modifying parameters or connecting additional AWS services.

---

## **Feedback**

If you encounter any issues or have suggestions for improvement, feel free to submit an issue in the repository. Happy learning! 🚀

---