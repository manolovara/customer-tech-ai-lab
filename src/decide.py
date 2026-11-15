import json

CATALOG = json.load(open("data/catalog.json", encoding="utf-8"))
SEGMENT_TO_PERSONA = {"developer": "pro_installer", "marketer": "home_owner",
                      "commerce": "deal_seeker"}

def persona_of(profile):
    """A persona exists only with a profile AND personalization consent."""
    if profile and profile["consent_personalization"] and profile["primary_segment"]:
        return SEGMENT_TO_PERSONA.get(profile["primary_segment"])
    return None

def next_best_offers(profile, category=None, n=3):
    persona = persona_of(profile)
    lead_hot = bool(persona and "lead_hot" in profile["primary_segment"])
    scored = []
    for it in CATALOG:
        score, why = 0.2 * it["popularity"], []
        if persona and persona in it["personas"]:
            score += 2
            why.append(f"fits your profile ({persona.replace('_', ' ')})")
        if lead_hot and it["type"] == "service":
            score += 1
            why.append("you asked to be contacted: services help you decide")
        if category and it["category"] == category:     # contextual: no consent needed
            score += 1
            why.append("related to the page you are viewing")
        offer = {k: it[k] for k in ("id", "name", "type", "price_eur")}
        scored.append((score, {**offer, "why": why or ["popular right now"]}))
    scored.sort(key=lambda s: s[0], reverse=True)
    return [o for _, o in scored[:n]]