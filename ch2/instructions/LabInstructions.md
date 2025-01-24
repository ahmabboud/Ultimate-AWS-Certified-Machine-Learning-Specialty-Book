
## AWS Glue Lab: Converting CSV to Parquet

### Objective
In this lab, you will convert a CSV file located in your GitHub repository to Parquet format using AWS Glue. This process involves setting up an S3 bucket, creating a Glue Crawler, and running an ETL job.

### Prerequisites
- An AWS account with administrator access.
- Basic understanding of AWS services.
- Familiarity with Python (helpful but not required).
- The CSV file located at `Ultimate-AWS-Certified-Machine-Learning-Specialty-Book/ch2/datasets/batch_data_sample.csv`.

### Step 1: Set Up Your Environment

1. **Sign in** to the AWS Management Console.
2. Ensure you are in your preferred region (e.g., `us-east-1`).

### Step 2: Create S3 Buckets

1. Navigate to **Amazon S3** in the AWS Console.
2. Click **Create bucket**.
3. Name your input bucket: `{your-account-id}-glue-lab-input` (replace `{your-account-id}` with your actual AWS account ID).
4. Leave other settings as default and click **Create bucket**.
5. Create another bucket for output named: `{your-account-id}-glue-lab-output`.

### Step 3: Upload the CSV File

1. Download the CSV file from your GitHub repository:
   - Navigate to `Ultimate-AWS-Certified-Machine-Learning-Specialty-Book/ch2/datasets/`.
   - Download `batch_data_sample.csv`.
2. Upload this CSV file to your input S3 bucket (`{your-account-id}-glue-lab-input`):
   - Open your input bucket in the S3 console.
   - Click **Upload**, then drag and drop the downloaded CSV file or select it from your file system.

### Step 4: Create an IAM Role for Glue

1. Go to **IAM** in the AWS Console.
2. Click **Roles** > **Create role**.
3. Choose **AWS service** as the trusted entity and select **Glue** as the use case.
4. Attach the following policies:
   - `AWSGlueServiceRole`
   - `AmazonS3FullAccess`
5. Name the role (e.g., `GlueLab-Role`) and click **Create role**.

### Step 5: Create a Glue Crawler

1. Navigate to **AWS Glue** in the console.
2. Go to **Crawlers** and click **Create crawler**.
3. Name your crawler (e.g., `CSV-Customer-Crawler`).
4. For data source:
   - Choose **S3** as the source type.
   - Select "In this account".
   - For the S3 path, browse and select your input bucket.
5. Select the IAM role you created earlier (`GlueLab-Role`).
6. For output:
   - Create a new database named `customerdb`.
7. Set the crawler schedule to "Run on demand".
8. Review and create the crawler.

### Step 6: Run the Crawler

1. Select your crawler and click **Run crawler**.
2. Wait for the crawler to finish; it will create a table in the Glue Data Catalog.

### Step 7: Create a Glue ETL Job

1. In AWS Glue, go to **Jobs** under "ETL Jobs" in the left sidebar.
2. Click **Script Editor** under **Create job** .
3. Choose **Spark** as the type and name your job (e.g., `CSV-to-Parquet-Conversion`).
4. Select the IAM role you created earlier (`GlueLab-Role`).
5. Under "This job runs", select "A new script to be authored by you".
6. Choose "Python" as the language.
7. In the script editor, paste the following code:

```python
# Import necessary libraries and modules
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# Retrieve job parameters
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Initialize Spark and Glue contexts
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Initialize Glue job
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read input data from the Glue Data Catalog
# This creates a DynamicFrame, which is a distributed collection of data
datasource = glueContext.create_dynamic_frame.from_catalog(
    database="customerdb",  # The database name in your Glue Data Catalog
    table_name="batch_data_sample"  # The table name created by your Glue Crawler
)

# Write the data to S3 in Parquet format
# This step converts the DynamicFrame to Parquet and saves it in your output S3 bucket
glueContext.write_dynamic_frame.from_options(
    frame=datasource,  # The input DynamicFrame
    connection_type="s3",  # Specifies that we're writing to S3
    connection_options={
        "path": "s3://{your-account-id}-glue-lab-output/customer-parquet/"
    },  # The S3 path where Parquet files will be saved
    format="parquet",  # Specifies the output format as Parquet
    format_options={"compression": "snappy"}  # Uses Snappy compression for Parquet files
)

# Commit the job
# This marks the job as completed and finalizes any operations
job.commit()
```

8. Replace `{your-account-id}` with your actual AWS account ID in the output path.
9. Replace `batch_data_sample` with the actual table name created by your crawler if different.
10. Save and create the job.

### Step 8: Run the ETL Job

1. Select your job and click **Run job**.
2. Monitor job progress in the Glue console.

### Step 9: Verify Results

1. Once the job completes, go to your output S3 bucket (`{your-account-id}-glue-lab-output`).
2. Navigate to `customer-parquet/`.
3. You should see Parquet files in this folder.

### Step 10: Clean Up Resources

To avoid unnecessary charges:
1. Delete both S3 buckets and their contents.
2. In AWS Glue, delete the database, crawler, and job.
3. In IAM, delete the role you created for this lab.

### Conclusion

You've successfully converted a CSV file from your GitHub repository into Parquet format using AWS Glue! This lab introduced you to key concepts such as crawlers, Data Catalogs, and ETL jobs within AWS Glue.

### Troubleshooting Tips

- If you encounter issues with permissions, ensure that your IAM role has sufficient access rights for both S3 and Glue operations.
- If the crawler fails, check that it can access files in your input S3 bucket.
- Review error logs in AWS Glue if any jobs fail during execution.
