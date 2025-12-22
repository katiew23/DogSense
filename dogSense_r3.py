#!/usr/bin/env python3

import time
import os
import json
from datetime import datetime
from picamera2 import Picamera2
from PIL import Image, ImageChops
from upload_cloudinary import upload_image
import BlynkLib
import paho.mqtt.publish as publish
import requests

SERVER_URL = "http://192.168.0.239:4000"
USER_ID = "451d22d1-a4ff-49d4-b6db-a752d571991d"

MQTT_BROKER = "localhost"
MQTT_TOPIC = "dogsense/events"

BLYNK_AUTH = os.getenv("BLYNK_AUTH")
blynk = BlynkLib.Blynk(BLYNK_AUTH)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
os.makedirs(STATIC_DIR, exist_ok=True)

IMAGE_PATH = os.path.join(STATIC_DIR, "last_visitor.jpg")
PREV_PATH = os.path.join(STATIC_DIR, "prev.jpg")
CURR_PATH = os.path.join(STATIC_DIR, "curr.jpg")

picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()

def capture(path):
    picam2.capture_file(path)

def movement_detected(img1, img2):
    return ImageChops.difference(img1, img2).getbbox() is not None

print("DogSense running")

time.sleep(2)
capture(PREV_PATH)
blynk.virtual_write(2, "Waiting for movement...")

last_event_time = 0

@blynk.on("V5")
def manual_capture(value):
    if int(value[0]) == 1:
        print("MANUAL CAPTURE BUTTON PRESSED")
        capture(IMAGE_PATH)
        image_url = upload_image(IMAGE_PATH)

        blynk.virtual_write(2, "Manual capture")

        requests.post(
            f"{SERVER_URL}/api/photo",
            json={
                "userId": USER_ID,
                "url": image_url
            }
        )
 
try:
    while True:
        blynk.run()
        time.sleep(0.1)

        now = time.time()
        if now - last_event_time < 3:
            continue

        capture(CURR_PATH)

        img1 = Image.open(PREV_PATH)
        img2 = Image.open(CURR_PATH)

        if movement_detected(img1, img2):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("MOVEMENT detected at", timestamp)

            blynk.virtual_write(0, 1)
            blynk.virtual_write(2, timestamp)

            capture(IMAGE_PATH)
            image_url = upload_image(IMAGE_PATH)

            requests.post(
                f"{SERVER_URL}/api/photo",
                json={
                    "userId": USER_ID,
                    "url": image_url
                }
            )

            requests.post(
                f"{SERVER_URL}/api/activity",
                json={
                    "userId": USER_ID,
                    "movement": 2,
                    "behaviour": 1
                }
            )

            event = {
                "deviceId": "dogsense_pi_01",
                "eventType": "movement_event",
                "timestamp": datetime.now().isoformat(),
                "imageUrl": image_url
                
            }
           

            blynk.virtual_write(1, image_url)

            publish.single(
                MQTT_TOPIC,
                json.dumps(event),
                hostname=MQTT_BROKER
            )

            last_event_time = now
            time.sleep(0.5)
            blynk.virtual_write(0, 0)

        os.replace(CURR_PATH, PREV_PATH)

except KeyboardInterrupt:
    pass

finally:
    picam2.stop()
