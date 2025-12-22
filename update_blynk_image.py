import time
import BlynkLib
import os

BLYNK_AUTH = os.getenv("BLYNK_AUTH")
blynk = BlynkLib.Blynk(BLYNK_AUTH)

BASE_URL = "https://res.cloudinary.com/dpzvpt5f1/image/upload/dogsense/last_visitor.jpg"

while True:
    # force a new URL every time
    url = BASE_URL + "?t=" + str(int(time.time()))

    blynk.virtual_write(1, url)

    print("Updated Blynk image URL:", url)

    time.sleep(5)
