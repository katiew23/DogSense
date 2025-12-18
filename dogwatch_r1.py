
import cv2
import time
import numpy as np
from picamera2 import Picamera2

print("DogSense Release 1 starting...")

#Camera
camera = Picamera2()
camera.configure(camera.create_preview_configuration())
camera.start()
time.sleep(2)

prev_frame = None
log_file = "movement_log.txt"


#MAIN LOOP

while True:
    frame = camera.capture_array()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if prev_frame is None:
        prev_frame = gray
        continue

    frame_delta = cv2.absdiff(prev_frame, gray)
    movement = int(np.sum(frame_delta) / 10000)

    prev_frame = gray

    if movement > 30:
        state = "DOG MOVING"
    else:
        state = "Calm"

    print(f"Movement={movement}, State={state}")

    with open(log_file, "a") as f:
        f.write(f"{time.time()}, {movement}, {state}\n")

    time.sleep(1)
