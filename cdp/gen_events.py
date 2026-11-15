import datetime, json, random, uuid

random.seed(7)
TOPICS = ["developer", "marketer", "commerce"]
PAGES = {"developer": "/docs/blocks", "marketer": "/docs/consent", "commerce": "/docs/checkout"}
t = datetime.datetime(2026, 11, 1, 9, 0)
events = []

def add(**kw):
    global t
    t += datetime.timedelta(minutes=random.randint(1, 40))
    events.append({"event_id": str(uuid.uuid4()), "ts": t.isoformat(), **kw})

for i in range(15):
    email = f"user{i}@example.com"
    main = random.choice(TOPICS)
    for _device in range(random.choice([1, 2])):      # same person, 1-2 devices
        anon = uuid.uuid4().hex[:8]
        for _view in range(random.randint(2, 6)):
            topic = main if random.random() < 0.8 else random.choice(TOPICS)
            add(type="page_view", anonymous_id=anon, topic=topic, page=PAGES[topic])
        add(type="login", anonymous_id=anon, email=email)   # links device to person
    add(type="consent_update", anonymous_id=anon, email=email,
        personalization=random.random() < 0.7)
    if random.random() < 0.4:
        add(type="form_submit", anonymous_id=anon, email=email, form="contact")

for _visitor in range(10):                              # anonymous visitors
    anon = uuid.uuid4().hex[:8]
    for _view in range(random.randint(1, 3)):
        topic = random.choice(TOPICS)
        add(type="page_view", anonymous_id=anon, topic=topic, page=PAGES[topic])

with open("data/events.jsonl", "w", encoding="utf-8") as f:
    for e in events:
        f.write(json.dumps(e) + "\n")
print(len(events), "events written")