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