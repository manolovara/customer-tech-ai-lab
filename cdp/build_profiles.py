"""Build unified customer profiles from data/events.jsonl -> data/profiles.json.

Identity resolution: every event carries an anonymous_id (one per device).
Events that also carry an email (login, consent_update, form_submit) link that
device to a person, so all of a device's events -- including page views made
before the login -- are stitched into that person's profile. Devices never
linked to an email stay as anonymous profiles.

Raw emails are not stored: profiles are keyed by email_hash (SHA-256 of the
lower-cased email), which is what src/ask_personalized.py looks up.

Run from the repo root:  python cdp/build_profiles.py
"""
import hashlib, json, sys
from collections import Counter, defaultdict

EVENTS = "data/events.jsonl"
OUT = "data/profiles.json"


def email_hash(email):
    return hashlib.sha256(email.strip().lower().encode()).hexdigest()


def load_events(path):
    with open(path, encoding="utf-8") as f:
        events = [json.loads(line) for line in f if line.strip()]
    return sorted(events, key=lambda e: e["ts"])


def resolve_identities(events):
    """anonymous_id -> email, from the first event that links them."""
    device_email, conflicts = {}, set()
    for e in events:
        email = e.get("email")
        if not email:
            continue
        email = email.strip().lower()
        known = device_email.setdefault(e["anonymous_id"], email)
        if known != email:
            conflicts.add(e["anonymous_id"])     # shared device: keep first owner
    for anon in sorted(conflicts):
        print(f"warning: device {anon} is linked to several emails; "
              f"its events are attributed to the first one", file=sys.stderr)
    return device_email


def build_profiles(events):
    device_email = resolve_identities(events)
    grouped = defaultdict(list)
    for e in events:
        anon = e["anonymous_id"]
        grouped[device_email.get(anon, f"anon:{anon}")].append(e)

    profiles = []
    for key, evs in grouped.items():
        known = not key.startswith("anon:")
        topics = Counter(e["topic"] for e in evs if e["type"] == "page_view" and e.get("topic"))
        consent = [e for e in evs if e["type"] == "consent_update"]
        # Most viewed topic; ties go to the topic viewed most recently.
        last_view = {e["topic"]: e["ts"] for e in evs if e["type"] == "page_view" and e.get("topic")}
        primary = max(topics, key=lambda t: (topics[t], last_view[t])) if topics else None

        profiles.append({
            "profile_id": email_hash(key)[:16] if known else key,
            "email_hash": email_hash(key) if known else None,
            "known": known,
            "anonymous_ids": sorted({e["anonymous_id"] for e in evs}),
            "first_seen": evs[0]["ts"],
            "last_seen": evs[-1]["ts"],
            "event_counts": dict(Counter(e["type"] for e in evs)),
            "topic_views": dict(topics.most_common()),
            "primary_segment": primary,
            # Latest consent decision wins; no decision recorded = no consent.
            "consent_personalization": bool(consent[-1].get("personalization")) if consent else False,
            "forms_submitted": sorted({e["form"] for e in evs if e["type"] == "form_submit" and e.get("form")}),
        })

    profiles.sort(key=lambda p: (not p["known"], p["first_seen"]))
    return profiles


if __name__ == "__main__":
    events = load_events(EVENTS)
    profiles = build_profiles(events)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=2)
    known = sum(p["known"] for p in profiles)
    print(f"{len(events)} events -> {len(profiles)} profiles "
          f"({known} known, {len(profiles) - known} anonymous) written to {OUT}")
