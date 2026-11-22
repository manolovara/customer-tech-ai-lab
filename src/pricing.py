import datetime, json

CATALOG = {it["id"]: it for it in json.load(open("data/catalog.json", encoding="utf-8"))}
ACCOUNTS = json.load(open("data/accounts.json", encoding="utf-8"))

VOLUME_BREAKS = [(50, 10.0), (25, 6.0), (10, 3.0), (0, 0.0)]   # devices -> % discount
TIER_DISCOUNT = {"bronze": 0.0, "silver": 3.0, "gold": 5.0}
AUTO_LIMIT = 15.0        # total discount up to here is approved automatically
MANAGER_LIMIT = 20.0     # up to here a manager approves; above, a director
VALIDITY_DAYS = 30

def volume_discount(devices):
    return next(pct for floor, pct in VOLUME_BREAKS if devices >= floor)

def build_quote(account_id, items, needs_installation=False,
                requested_discount_pct=None, today=None):
    acct = ACCOUNTS[account_id]
    today = today or datetime.date.today()
    qty, clarifications = {}, []
    for it in items:
        pid, n = it.get("product_id"), it.get("quantity", 0)
        if pid not in CATALOG or not isinstance(n, int) or n <= 0:
            clarifications.append(f"Could not use request line: {pid!r} x {n!r}")
            continue
        qty[pid] = qty.get(pid, 0) + n
    devices = sum(n for pid, n in qty.items() if CATALOG[pid]["type"] == "product")
    if needs_installation and devices:
        qty["install-basic"] = devices                 # one installation per device

    lines = []
    for pid, n in qty.items():
        unit = round(CATALOG[pid]["wholesale_eur"] * 100)          # cents
        lines.append({"id": pid, "name": CATALOG[pid]["name"], "type": CATALOG[pid]["type"],
                      "quantity": n, "unit_eur": unit / 100, "line_eur": unit * n / 100,
                      "_cents": unit * n})
    subtotal = sum(l["_cents"] for l in lines)

    standard = volume_discount(devices) + TIER_DISCOUNT[acct["tier"]]
    target = max(standard, float(requested_discount_pct or 0))
    if target <= AUTO_LIMIT:
        status, applied = "approved", target
    elif target <= MANAGER_LIMIT:
        status, applied = "pending_manager", standard   # price at standard until approved
    else:
        status, applied = "pending_director", standard
    if not lines:
        status = "needs_clarification"

    discount = round(subtotal * applied / 100)
    suggestions = []
    if devices and "care-plan" not in qty:
        suggestions.append({"id": "care-plan", "name": CATALOG["care-plan"]["name"],
                            "why": "Extends the warranty to 36 months and covers yearly maintenance"})
    return {
        "account_id": account_id, "account": acct["name"], "tier": acct["tier"],
        "currency": "EUR", "vat": "excluded",
        "lines": [{k: v for k, v in l.items() if k != "_cents"} for l in lines],
        "subtotal_eur": subtotal / 100,
        "standard_discount_pct": standard, "requested_discount_pct": requested_discount_pct,
        "target_pct": target, "discount_pct": applied,
        "discount_eur": discount / 100, "total_eur": (subtotal - discount) / 100,
        "total_if_approved_eur": (subtotal - round(subtotal * target / 100)) / 100,
        "status": status,
        "valid_until": (today + datetime.timedelta(days=VALIDITY_DAYS)).isoformat(),
        "clarifications": clarifications, "suggestions": suggestions,
    }