import argparse, hashlib, json
from ask import answer

def load_profile(email):
    h = hashlib.sha256(email.lower().encode()).hexdigest()
    for p in json.load(open("data/profiles.json", encoding="utf-8")):
        if p.get("email_hash") == h:
            return p
    return None

ap = argparse.ArgumentParser()
ap.add_argument("question")
ap.add_argument("--email")
ap.add_argument("--groups", default="public")
a = ap.parse_args()

profile = load_profile(a.email) if a.email else None
audience = hint = None
if profile and profile["consent_personalization"] and profile["primary_segment"]:
    audience = profile["primary_segment"]
    hint = f"The reader is a {audience}. Use vocabulary and examples suited to that audience."
    print(f"[personalization ON: segment={audience}]")
else:
    print("[personalization OFF: no profile or no consent]")

text, hits = answer(a.question, a.groups.split(","), audience, hint)
print(text, "\n\nSources:")
for i, h in enumerate(hits, 1):
    print(f"[{i}] {h['title']} ({h['source']})")