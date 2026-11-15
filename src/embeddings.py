import json
import numpy as np
from config import *

_local = None
_br = None

def embed_many(texts):
    global _local, _br
    if EMBED_BACKEND == "local":
        if _local is None:
            from fastembed import TextEmbedding
            _local = TextEmbedding(model_name=LOCAL_EMBED_MODEL)
        return [np.asarray(v, dtype=float).tolist() for v in _local.embed(texts)]
    import boto3                                    # solo si EMBED_BACKEND=bedrock
    if _br is None:
        _br = boto3.client("bedrock-runtime", region_name=AWS_REGION)
    out = []
    for t in texts:
        r = _br.invoke_model(modelId=EMBED_MODEL, body=json.dumps(
            {"inputText": t, "dimensions": EMBED_DIMS, "normalize": True}))
        out.append(json.loads(r["body"].read())["embedding"])
    return out

def embed(text):
    return embed_many([text])[0]