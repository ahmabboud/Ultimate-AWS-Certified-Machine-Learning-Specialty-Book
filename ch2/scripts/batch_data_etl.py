import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Load batch data from S3
datasource = glueContext.create_dynamic_frame.from_catalog(database="batch_data_db", table_name="your_table_name")

# Write the raw data to another S3 bucket
glueContext.write_dynamic_frame.from_options(
    frame=datasource,
    connection_type="s3",
    connection_options={"path": "s3://processed-batch-data/raw/"},
    format="parquet"
)

job.commit()
