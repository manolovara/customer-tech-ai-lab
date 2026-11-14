import csv, json, pathlib, re
import boto3
from config import *
from vectorstore import get_store

LEVEL = {"public": 0, "partner": 1, "internal": 2}
br = boto3.client("bedrock-runtime", region_name=AWS_REGION)

def embed(text):
    r = br.invoke_model(modelId=EMBED_MODEL, body=json.dumps(
        {"inputText": text, "dimensions": EMBED_DIMS, "normalize": True}))
    return json.loads(r["body"].read())["embedding"]

def chunk(text, size=900, overlap=150):
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks, cur = [], ""
    for p in paras:
        if cur and len(cur) + len(p) > size:
            chunks.append(cur)
            cur = cur[-overlap:] + "\n\n" + p
        else:
            cur = f"{cur}\n\n{p}" if cur else p
    if cur:
        chunks.append(cur)
    return chunks

chunks, vectors = [], []
for row in csv.DictReader(open("data/manifest.csv", encoding="utf-8")):
    text = pathlib.Path("data/docs", row["file"]).read_text(encoding="utf-8")
    stem = re.sub(r"[^A-Za-z0-9_-]", "-", pathlib.Path(row["file"]).stem)
    for i, c in enumerate(chunk(text)):
        key = f"{stem}-{i}"
        meta = {"source": row["file"], "audience": row["audience"], "level": LEVEL[row["allowed_groups"]]}
        chunks.append({"id": key, "title": row["title"], "text": c, **meta})
        vectors.append({"key": key, "data": {"float32": embed(c)},
                        "metadata": {**meta, "title": row["title"], "text": c}})

get_store().upsert(vectors)          # S3 Vectors o almacén local, según VECTOR_BACKEND

json.dump(chunks, open("data/chunks.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(f"{len(vectors)} chunks indexed ({VECTOR_BACKEND})")