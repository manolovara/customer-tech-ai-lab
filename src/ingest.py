import csv, json, pathlib, re
from config import *
from embeddings import embed_many
from vectorstore import get_store

LEVEL = {"public": 0, "partner": 1, "internal": 2}

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
    parts = chunk(text)
    for i, (c, vec) in enumerate(zip(parts, embed_many(parts))):
        key = f"{stem}-{i}"
        meta = {"source": row["file"], "audience": row["audience"],
                "level": LEVEL[row["allowed_groups"]]}
        chunks.append({"id": key, "title": row["title"], "text": c, **meta})
        vectors.append({"key": key, "data": {"float32": vec},
                        "metadata": {**meta, "title": row["title"], "text": c}})

get_store().upsert(vectors)          # almacén local o S3 Vectors, según VECTOR_BACKEND

json.dump(chunks, open("data/chunks.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(f"{len(vectors)} chunks indexed (embeddings={EMBED_BACKEND}, store={VECTOR_BACKEND})")