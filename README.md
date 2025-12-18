DogSense – Release 3

DogSense is an IoT prototype for monitoring dog activity using a Raspberry Pi, a camera, and a backend processing service.

Release 3 Overview

Release 3 extends DogSense from a single edge-device solution to a multi-component IoT system.

In this release, movement events detected on the Raspberry Pi are published using MQTT to a backend service.
The backend subscribes to these events, stores them persistently, and applies simple rule-based logic to detect high activity.

This introduces backend processing, historical data storage, and intelligent behaviour beyond basic sensing.

System Behaviour

When movement is detected:

The Raspberry Pi captures an image

The image is uploaded to Cloudinary

A structured event is published to an MQTT topic

A backend service receives the event

The event is stored in a SQLite database

Alerts are generated when high activity is detected

Technologies Used

Raspberry Pi OS (Linux)

Python

PiCamera2

MQTT (Mosquitto)

SQLite

Cloudinary

TCP/IP networking

Files

dogwatch_r2.py – Edge device application (movement detection + MQTT publish)

backend_listener.py – Backend MQTT subscriber and event processor

upload_cloudinary.py – Image upload helper

dogwatch_r1.py – Release 1 baseline implementation

Architecture

Raspberry Pi (edge device) → MQTT Broker → Backend Service → SQLite Database

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
