import csv, json, pathlib

FIELDS = ["file", "title", "source", "audience", "allowed_groups"]

items = json.load(open("data/catalog.json", encoding="utf-8"))
manifest = pathlib.Path("data/manifest.csv")
with manifest.open(encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

generated = []
for it in items:
    files = {
        f"product-{it['id']}.md": (
            f"# {it['name']}\n\nType: {it['type']}. Category: {it['category']}.\n\n"
            f"{it['desc']}\n\nPublic price: {it['price_eur']} EUR. "
            f"Tags: {', '.join(it['tags'])}.\n", "public"),
        f"partner-price-{it['id']}.md": (
            f"# Installer pricing: {it['name']}\n\nWholesale price for certified "
            f"installers: {it['wholesale_eur']} EUR (partner portal only).\n", "partner"),
    }
    for fname, (body, group) in files.items():
        pathlib.Path("data/docs", fname).write_text(body, encoding="utf-8")
        generated.append({"file": fname, "title": it["name"], "source": fname,
                          "audience": "all", "allowed_groups": group})

# Replace this script's rows (also repairs rows written by older versions);
# keep every hand-written row untouched.
names = {g["file"] for g in generated}
rows = [r for r in rows if r["file"] not in names] + generated

with manifest.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
    w.writeheader()
    w.writerows({k: r[k] for k in FIELDS} for r in rows)
print(f"{len(generated)} documents written")
