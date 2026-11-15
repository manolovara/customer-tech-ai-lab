import csv
from ask import answer, REFUSAL

RESTRICTED = {"partner-pricing.md": "partner", "internal-roadmap.md": "internal"}
rows = list(csv.DictReader(open("eval/golden-set.csv", encoding="utf-8")))
hit = refused_ok = leaks = n_ans = n_ref = 0

for r in rows:
    groups = r["groups"].split(";")
    text, hits = answer(r["question"], groups)
    srcs = [h["source"] for h in hits]
    leaks += any(s in RESTRICTED and RESTRICTED[s] not in groups for s in srcs)
    if r["must_refuse"] == "yes":
        n_ref += 1
        refused_ok += text.strip() == REFUSAL
    else:
        n_ans += 1
        hit += r["expected_source"] in srcs
        print(f"- {r['question']}\n  -> {text[:160]!r}\n  sources: {srcs}")

print(f"\nhit@4: {hit}/{n_ans} | correct refusals: {refused_ok}/{n_ref} | leaks: {leaks}")