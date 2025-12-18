import RPi.GPIO as GPIO
import time

PIR_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("Starting PIR test. Press Ctrl+C to stop.")

try:
    while True:
        value = GPIO.input(PIR_PIN)
        print("RAW PIR VALUE:", value)
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Stopped")

