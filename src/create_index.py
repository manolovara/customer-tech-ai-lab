import boto3
from botocore.exceptions import ClientError
from config import *

s3v = boto3.client("s3vectors", region_name=AWS_REGION)

def create_once(fn, **kwargs):
    try:
        fn(**kwargs)
        print("created:", list(kwargs.values())[0])
    except ClientError as e:
        code = e.response["Error"]["Code"]
        if "Conflict" in code or "AlreadyExists" in code:
            print("already exists, continuing")
        else:
            raise

create_once(s3v.create_vector_bucket, vectorBucketName=VECTOR_BUCKET)
create_once(
    s3v.create_index,
    vectorBucketName=VECTOR_BUCKET, indexName=VECTOR_INDEX,
    dataType="float32", dimension=EMBED_DIMS, distanceMetric="cosine",
    metadataConfiguration={"nonFilterableMetadataKeys": ["text", "title"]},
)