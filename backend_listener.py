import json
import sqlite3
import paho.mqtt.client as mqtt

MQTT_BROKER = "localhost"
MQTT_TOPIC = "dogsense/events"
DB_FILE = "dogsense.db"

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT,
    event_type TEXT,
    timestamp TEXT,
    image_url TEXT
)
""")
conn.commit()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())

    cur.execute(
        """
        INSERT INTO events (device_id, event_type, timestamp, image_url)
        VALUES (?, ?, ?, ?)
        """,
        (
            data["deviceId"],
            data["eventType"],
            data["timestamp"],
            data["imageUrl"]
        )
    )
    conn.commit()

    cur.execute("""
        SELECT COUNT(*) FROM events
        WHERE timestamp >= datetime('now', '-1 minute')
    """)
    count = cur.fetchone()[0]

    if count >= 3:
        print("ALERT: High activity detected")

    print("Saved event to DB")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER)
client.loop_forever()
