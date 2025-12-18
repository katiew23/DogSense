import RPi.GPIO as GPIO
import time

SOUND_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(SOUND_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # important

print("Raw pin reading. Clap and watch it change (0/1). Ctrl+C to stop.")

try:
    while True:
        val = GPIO.input(SOUND_PIN)
        print(val)
        time.sleep(0.05)
except KeyboardInterrupt:
    GPIO.cleanup()

