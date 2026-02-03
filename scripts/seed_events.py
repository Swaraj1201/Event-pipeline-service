import random
from datetime import datetime, timedelta
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.event_pipeline

sources = ["sensor-1", "api-gateway", "auth-service", "billing"]
types = ["login_failure", "rate_limit", "temperature", "payment"]

def random_event():
    return {
        "source": random.choice(sources),
        "event_type": random.choice(types),
        "payload": {
            "value": random.randint(1, 100),
            "message": "synthetic event"
        },
        "timestamp": datetime.utcnow() - timedelta(
            minutes=random.randint(0, 10000)
        )
    }

events = [random_event() for _ in range(800)]
db.events.insert_many(events)

print("Seeded events successfully")
