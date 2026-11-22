import datetime, pathlib, shutil, tempfile
import booking as bk

tmp = pathlib.Path(tempfile.mkdtemp())
shutil.copy("data/slots.json", tmp / "slots.json")
bk.SLOTS_PATH, bk.BOOKINGS_PATH = tmp / "slots.json", tmp / "bookings.json"

A, B, C = "user0@example.com", "user2@example.com", "user3@example.com"
# A and B live in Madrid and have a Care Plan; C is outside the service area.

r = bk.find_slots(A, "maintenance")
assert r["slots"] and r["price_eur"] == 0                       # Care Plan covers maintenance
assert bk.price_for("user1@example.com", "maintenance") == 79    # no Care Plan: full price
assert bk.find_slots(C, "install") == {"error": "out_of_area"}

slot = r["slots"][0]["slot_id"]
b1 = bk.commit_booking(A, slot, "maintenance", "key-1")
assert b1["status"] == "confirmed"
assert bk.commit_booking(A, slot, "maintenance", "key-1")["booking_id"] == b1["booking_id"]   # idempotent
assert bk.commit_booking(B, slot, "maintenance", "key-2") == {"error": "slot_no_longer_available"}
assert bk.check_proposal(B, slot, "maintenance") == {"error": "slot_no_longer_available"}

assert bk.quote_cancellation(B, b1["booking_id"]) == {"error": "not_found"}   # not B's booking
d = datetime.datetime
assert bk.cancel_fee("2030-01-10T09:00", d(2030, 1, 8, 9, 0)) == 0               # 48 h before
assert bk.cancel_fee("2030-01-10T09:00", d(2030, 1, 9, 10, 0)) == 30             # 23 h before

c = bk.commit_cancellation(A, b1["booking_id"], now=d(2000, 1, 1))
assert c["status"] == "cancelled" and c["fee_eur"] == 0
assert bk.quote_cancellation(A, b1["booking_id"]) == {"error": "not_found"}      # already cancelled
assert bk.commit_booking(B, slot, "maintenance", "key-3")["status"] == "confirmed"   # slot freed
print("all booking tests passed")