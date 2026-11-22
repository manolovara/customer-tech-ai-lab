from pricing import build_quote

def q(items, **kw):
    return build_quote("acme-install", items, **kw)       # acme-install is gold (5%)

HUB10 = [{"product_id": "hub-pro", "quantity": 10}]

a = q(HUB10)
assert a["standard_discount_pct"] == 8.0                   # 3% volume + 5% gold
assert (a["status"], a["subtotal_eur"], a["total_eur"]) == ("approved", 1790.0, 1646.8)

b = q(HUB10, requested_discount_pct=18)                    # above the automatic limit
assert (b["status"], b["discount_pct"], b["total_eur"], b["total_if_approved_eur"]) == \
    ("pending_manager", 8.0, 1646.8, 1467.8)

c = q(HUB10, requested_discount_pct=40)
assert c["status"] == "pending_director" and c["discount_pct"] == 8.0

d = q([{"product_id": "hub-pro", "quantity": 2}], needs_installation=True)
assert [l["id"] for l in d["lines"]] == ["hub-pro", "install-basic"]
assert (d["subtotal_eur"], d["total_eur"]) == (556.0, 528.2)

e = q([{"product_id": "solar-inverter", "quantity": 3}])
assert e["status"] == "needs_clarification" and e["clarifications"]

f = q([{"product_id": "hub-pro", "quantity": -5}])
assert f["status"] == "needs_clarification"

g = q(HUB10, requested_discount_pct=0)
assert g["total_eur"] == 1646.8                            # never below the standard discount
print("all pricing tests passed")