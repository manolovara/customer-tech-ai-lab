import datetime, json, pathlib, uuid

SERVICES = {s["id"]: s for s in json.load(open("data/services.json", encoding="utf-8"))}
TECHS = {t["id"]: t for t in json.load(open("data/technicians.json", encoding="utf-8"))}
CUSTOMERS = json.load(open("data/customers.json", encoding="utf-8"))
SLOTS_PATH = pathlib.Path("data/slots.json")
BOOKINGS_PATH = pathlib.Path("data/bookings.json")
LATE_CANCEL_HOURS = 24
LATE_CANCEL_FEE_EUR = 30

def _load(path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default

def _save(path, data):
    path.write_text(json.dumps(data, indent=1), encoding="utf-8")

def price_for(email, service_id):
    s = SERVICES[service_id]
    return s["care_plan_price_eur"] if CUSTOMERS[email]["care_plan"] else s["price_eur"]

def _eligible(email, service_id, tech_id):
    t, s = TECHS[tech_id], SERVICES[service_id]
    return CUSTOMERS[email]["postcode"][:2] in t["areas"] and s["skill"] in t["skills"]

SERVICE_AREAS = "the Madrid and Valencia provinces"
OUT_OF_AREA = {"error": "out_of_area",
               "message": f"This address is outside our service area. We currently serve "
                          f"{SERVICE_AREAS}. Offer to hand the customer over to a human agent."}

def in_service_area(email):
    return any(CUSTOMERS[email]["postcode"][:2] in t["areas"] for t in TECHS.values())

def find_slots(email, service_id, earliest=None, n=4):
    if not in_service_area(email):
        return dict(OUT_OF_AREA)
    if not any(_eligible(email, service_id, t) for t in TECHS):
        return {"error": "no_technician_for_this_service_in_your_area"}
    try:
        earliest = datetime.date.fromisoformat(earliest).isoformat()
    except (TypeError, ValueError):
        earliest = datetime.date.today().isoformat()
    free = [x for x in _load(SLOTS_PATH, []) if x["status"] == "free"
            and x["start"][:10] >= earliest and _eligible(email, service_id, x["tech_id"])]
    free.sort(key=lambda x: x["start"])
    return {"slots": [{"slot_id": x["slot_id"], "start": x["start"]} for x in free[:n]],
            "price_eur": price_for(email, service_id)}

def check_proposal(email, slot_id, service_id):
    if service_id not in SERVICES:
        return {"error": "unknown_service"}
    slot = next((x for x in _load(SLOTS_PATH, []) if x["slot_id"] == slot_id), None)
    if not slot or slot["status"] != "free":
        return {"error": "slot_no_longer_available"}
    if not _eligible(email, service_id, slot["tech_id"]):
        return {"error": "slot_not_valid_for_this_customer"}
    s = SERVICES[service_id]
    return {"service_id": service_id, "service": s["name"], "slot_id": slot_id,
            "start": slot["start"], "duration_min": s["duration_min"],
            "price_eur": price_for(email, service_id)}

def commit_booking(email, slot_id, service_id, key):
    bookings = _load(BOOKINGS_PATH, {})
    for b in bookings.values():
        if b["idempotency_key"] == key:                  # same request again: same result
            return b
    check = check_proposal(email, slot_id, service_id)   # re-validate at commit time
    if "error" in check:
        return check
    slots = _load(SLOTS_PATH, [])
    next(x for x in slots if x["slot_id"] == slot_id)["status"] = "booked"
    booking = {"booking_id": "B-" + uuid.uuid4().hex[:8], "email": email,
               "service_id": service_id, "slot_id": slot_id, "start": check["start"],
               "price_eur": check["price_eur"], "status": "confirmed", "idempotency_key": key}
    bookings[booking["booking_id"]] = booking
    _save(SLOTS_PATH, slots)
    _save(BOOKINGS_PATH, bookings)
    return booking

def cancel_fee(start_iso, now):
    hours = (datetime.datetime.fromisoformat(start_iso) - now).total_seconds() / 3600
    return 0 if hours >= LATE_CANCEL_HOURS else LATE_CANCEL_FEE_EUR

def quote_cancellation(email, booking_id, now=None):
    now = now or datetime.datetime.now()
    b = _load(BOOKINGS_PATH, {}).get(booking_id)
    if not b or b["email"] != email or b["status"] != "confirmed":
        return {"error": "not_found"}                    # same answer for other people's bookings
    return {"booking_id": booking_id, "start": b["start"],
            "fee_eur": cancel_fee(b["start"], now)}

def commit_cancellation(email, booking_id, now=None):
    q = quote_cancellation(email, booking_id, now)
    if "error" in q:
        return q
    bookings = _load(BOOKINGS_PATH, {})
    bookings[booking_id]["status"] = "cancelled"
    slots = _load(SLOTS_PATH, [])
    for x in slots:
        if x["slot_id"] == bookings[booking_id]["slot_id"]:
            x["status"] = "free"
    _save(BOOKINGS_PATH, bookings)
    _save(SLOTS_PATH, slots)
    return {**q, "status": "cancelled"}

def list_bookings(email):
    hidden = ("email", "idempotency_key")
    return [{k: v for k, v in b.items() if k not in hidden}
            for b in _load(BOOKINGS_PATH, {}).values()
            if b["email"] == email and b["status"] == "confirmed"]