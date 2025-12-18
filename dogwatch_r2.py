#!/usr/bin/env python3

import time
import os
from datetime import datetime
from picamera2 import Picamera2
from PIL import Image, ImageChops
from upload_cloudinary import upload_image
import BlynkLib

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

print("DogSense Release 2 running (camera + Blynk)")

def capture(path):
    picam2.capture_file(path)

def movement_detected(img1, img2):
    return ImageChops.difference(img1, img2).getbbox() is not None

time.sleep(2)
capture(PREV_PATH)
blynk.virtual_write(2, "Waiting for movement...")

last_event_time = 0

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

            blynk.virtual_write(0, 1)        # LED
            blynk.virtual_write(2, timestamp)  # ✅ LAST MOVEMENT (V2)

            capture(IMAGE_PATH)
            upload_image(IMAGE_PATH)

            last_event_time = now
            time.sleep(0.5)
            blynk.virtual_write(0, 0)

        os.replace(CURR_PATH, PREV_PATH)

except KeyboardInterrupt:
    pass

finally:
    picam2.stop()
