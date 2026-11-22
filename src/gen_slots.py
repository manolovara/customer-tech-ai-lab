import datetime, json, random

random.seed(11)
techs = json.load(open("data/technicians.json", encoding="utf-8"))
start = datetime.date.today() + datetime.timedelta(days=1)
slots, n = [], 0
for d in range(14):
    day = start + datetime.timedelta(days=d)
    if day.weekday() >= 5:
        continue                                          # no weekend visits
    for t in techs:
        for hhmm in ("09:00", "11:30", "14:00"):
            if random.random() < 0.25:
                continue                                  # technician busy
            n += 1
            slots.append({"slot_id": f"S{n:04d}", "tech_id": t["id"],
                          "start": f"{day.isoformat()}T{hhmm}", "status": "free"})
json.dump(slots, open("data/slots.json", "w", encoding="utf-8"), indent=1)
print(len(slots), "slots generated")