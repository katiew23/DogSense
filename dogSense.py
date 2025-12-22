#!/usr/bin/env python3

import time
import os
import json
from datetime import datetime
from picamera2 import Picamera2
from PIL import Image, ImageChops
from sense_hat import SenseHat
from upload_cloudinary import upload_image
import BlynkLib
import paho.mqtt.publish as publish

# Setup
sense = SenseHat()
gallery_index = 0
last_event_time = 0

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

# Helper functions
def capture(path):
    picam2.capture_file(path)

def movement_detected(img1, img2):
    return ImageChops.difference(img1, img2).getbbox() is not None

def shake_detected(threshold=0.8):
    accel = sense.get_accelerometer_raw()
    return (
        abs(accel['x']) > threshold or
        abs(accel['y']) > threshold or
        abs(accel['z']) > threshold
    )

def bump_gallery():
    global gallery_index
    gallery_index = 1 - gallery_index
    blynk.virtual_write(1, gallery_index)

def handle_event(event_type):
    global last_event_time

    capture(IMAGE_PATH)
    image_url = upload_image(IMAGE_PATH)
    bump_gallery()

    event = {
        "deviceId": "dogsense_pi_01",
        "eventType": event_type,
        "timestamp": datetime.now().isoformat(),
        "imageUrl": image_url
    }

    publish.single(MQTT_TOPIC, json.dumps(event), hostname=MQTT_BROKER)

    blynk.virtual_write(0, 1)
    blynk.virtual_write(2, event_type)
    time.sleep(0.5)
    blynk.virtual_write(0, 0)

    last_event_time = time.time()

# Blynk manual button
@blynk.on("V5")
def manual_capture(value):
    print("Manual button pressed:", value)
    if int(value[0]) == 1:
        handle_event("manual_capture")

# Main loop
print("DogSense running")
time.sleep(2)
capture(PREV_PATH)
blynk.virtual_write(2, "Waiting for movement...")

try:
    while True:
        blynk.run()
        time.sleep(0.1)

        if time.time() - last_event_time < 1:
            continue

        capture(CURR_PATH)
        img1 = Image.open(PREV_PATH)
        img2 = Image.open(CURR_PATH)

        if movement_detected(img1, img2):
           print("Camera movement detected") 
           handle_event("camera_movement")

        if shake_detected():
            print("Shake detected")
            handle_event("device_shake")

        os.replace(CURR_PATH, PREV_PATH)

except KeyboardInterrupt:
    pass

finally:
    picam2.stop()
