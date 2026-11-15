import json
import boto3
import numpy as np
from config import *

class S3VectorsStore:
    def __init__(self):
        self.c = boto3.client("s3vectors", region_name=AWS_REGION)

    def upsert(self, vectors):
        for i in range(0, len(vectors), 100):
            self.c.put_vectors(vectorBucketName=VECTOR_BUCKET, indexName=VECTOR_INDEX,
                               vectors=vectors[i:i + 100])

    def query(self, qvec, level, audience, k):
        flt = {"level": {"$lte": level}}                  # security trimming
        if audience:                                       # personalization
            flt = {"$and": [flt, {"audience": {"$in": ["all", audience]}}]}
        r = self.c.query_vectors(vectorBucketName=VECTOR_BUCKET, indexName=VECTOR_INDEX,
                                 queryVector={"float32": qvec}, topK=k,
                                 filter=flt, returnMetadata=True)
        return [v["key"] for v in r["vectors"]]

class LocalStore:
    PATH = "data/vectors.json"

    def upsert(self, vectors):
        data = {v["key"]: {"vec": v["data"]["float32"],
                           "level": v["metadata"]["level"],
                           "audience": v["metadata"]["audience"]} for v in vectors}
        json.dump(data, open(self.PATH, "w", encoding="utf-8"))

    def query(self, qvec, level, audience, k):
        data = json.load(open(self.PATH, encoding="utf-8"))
        # Same filters as S3 Vectors, applied BEFORE scoring (pre-filtering).
        keys = [key for key, d in data.items()
                if d["level"] <= level and (not audience or d["audience"] in ("all", audience))]
        if not keys:
            return []
        m = np.array([data[key]["vec"] for key in keys])
        q = np.array(qvec)
        sims = (m @ q) / (np.linalg.norm(m, axis=1) * np.linalg.norm(q))
        return [keys[i] for i in np.argsort(-sims)[:k]]

def get_store():
    return LocalStore() #if VECTOR_BACKEND == "local" else S3VectorsStore()