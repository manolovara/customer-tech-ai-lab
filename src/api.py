import datetime, hashlib, json
from fastapi import FastAPI  # pyright: ignore[reportMissingImports]
from fastapi.responses import FileResponse  # pyright: ignore[reportMissingImports]
from pydantic import BaseModel
from ask import answer, REFUSAL
from decide import next_best_offers, persona_of
from quote_api import router as quote_router
from booking_api import router as booking_router

app = FastAPI()
app.include_router(quote_router)
app.include_router(booking_router)
PROFILES = json.load(open("data/profiles.json", encoding="utf-8"))
ROLE_GROUPS = {"visitor": ["public"], "partner": ["public", "partner"]}  # prod: from the auth token
HERO = {
    "pro_installer": {"title": "Build once, install everywhere",
                      "subtitle": "Open API, installer pricing and certification."},
    "home_owner": {"title": "Cut your energy bill this winter",
                   "subtitle": "Smart climate and energy devices, installed for you."},
    "deal_seeker": {"title": "This week's best value picks",
                    "subtitle": "Popular devices and services at clear prices."},
    None: {"title": "Smart homes, made simple",
           "subtitle": "Products and services for every home."},
}

def find_profile(email):
    if not email:
        return None
    h = hashlib.sha256(email.lower().encode()).hexdigest()
    return next((p for p in PROFILES if p.get("email_hash") == h), None)

@app.get("/")
def home():
    return FileResponse("web/index.html")

@app.get("/api/experience")
def experience(email: str = "", consent: bool = True, category: str = ""):
    profile = find_profile(email)
    active = profile if (profile and consent) else None   # browser toggle can only reduce
    persona = persona_of(active)
    if persona:
        explain = (f"Personalized from your profile (segment: {active['primary_segment']}), "
                   "because you gave consent.")
    elif not profile:
        explain = "Generic experience: anonymous visitor."
    elif not profile["consent_personalization"]:
        explain = "Generic experience: no personalization consent on file."
    elif not consent:
        explain = "Generic experience: you withdrew consent in this browser."
    else:
        explain = "Generic experience: not enough activity to personalize yet."
    return {"personalized": bool(persona), "persona": persona, "hero": HERO[persona],
            "offers": next_best_offers(active, category or None), "explain": explain}

class AskBody(BaseModel):
    question: str
    email: str = ""
    role: str = "visitor"
    consent: bool = True

@app.post("/api/ask")
def ask_endpoint(body: AskBody):
    profile = find_profile(body.email) if body.consent else None
    persona = persona_of(profile)
    hint = ("Never invent prices, discounts or availability; quote them only from the "
            "sources. Keep the answer under 120 words.")
    if persona:
        hint += f" The visitor is a {persona.replace('_', ' ')}: use relevant examples."
    text, hits = answer(body.question, ROLE_GROUPS.get(body.role, ["public"]),
                        profile["primary_segment"] if persona else None, hint)
    sources = [] if text == REFUSAL else sorted({h["source"] for h in hits})   # cite only real answers
    return {"answer": text, "sources": sources,
            "personalized": bool(persona)}

class LeadBody(BaseModel):
    email: str = ""
    interest: str = ""
    consent: bool = False          # explicit contact consent, separate from personalization

@app.post("/api/lead")
def lead(body: LeadBody):
    if not body.consent:
        return {"status": "not_sent", "reason": "no contact consent"}
    profile = find_profile(body.email)
    if not profile:
        return {"status": "not_sent", "reason": "pick a known visitor for the demo"}
    payload = {"ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "unified_id": profile["profile_id"], "interest": body.interest,
               "segments": profile["primary_segment"] if profile["consent_personalization"] else [],
               "channel": "crm"}
    with open("data/leads.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(payload) + "\n")
    return {"status": "sent_to_crm_stub", "payload": payload}