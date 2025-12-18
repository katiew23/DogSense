# DogSense – Release 2

DogSense is an IoT prototype for monitoring dog activity using a Raspberry Pi and a camera.

## Release 2 Overview
This release implements camera-based movement detection on a Raspberry Pi edge device.  
When movement is detected, the device sends structured event data to the Blynk cloud platform.

A live web dashboard displays:
- Current movement state
- Timestamp of the last detected movement
- Historical movement graph

## Technologies Used
- Raspberry Pi OS (Linux)
- Python
- PiCamera2
- Blynk IoT Platform
- TCP/IP networking

## Files
- `dogwatch_r2.py` – Release 2 application code
- `upload_cloudinary.py` – Image upload helper
- `dogwatch_r1.py` – Release 1 baseline implementation

## Architecture
Raspberry Pi (edge device) → Blynk Cloud → Web Dashboard
