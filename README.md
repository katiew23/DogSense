DogSense – Release 3b
Project Overview

DogSense is an IoT prototype for monitoring dog activity while the owner is away.
It uses a Raspberry Pi with sensors and a camera to detect movement, capture images, and present updates remotely via a mobile app.

The system is event-driven and cloud-connected, focusing on practical IoT concepts rather than a custom-built dashboard.

Release 3 Overview

Release 3 represents the final version of DogSense.

In this release, the Raspberry Pi acts as an edge device that detects movement, captures images, uploads them to the cloud, and updates a mobile interface in real time. Rather than building a custom web dashboard, the Blynk IoT platform was selected to provide a reliable, mobile-first user interface.

Cloudinary is used for persistent image storage and delivery.

This release demonstrates a complete IoT workflow including sensing, processing, cloud integration, and remote monitoring.

System Behaviour

When movement is detected:

The Raspberry Pi detects motion using sensors

An image is captured using the Pi camera

The image is uploaded to Cloudinary

The Cloudinary image URL is updated in the Blynk app

The latest image is displayed on the mobile interface

This allows the user to remotely view the most recent activity without direct access to the device.

Technologies Used

Raspberry Pi OS (Linux)

Python

PiCamera2

Blynk IoT Platform

Cloudinary

TCP/IP networking

Files

dogSense_r3.py – Main edge-device application (motion detection, image capture, Blynk integration)

upload_cloudinary.py – Helper module for uploading images to Cloudinary

pi_server.py – Supporting service logic for device-side processing

dogwatch_r1.py – Release 1 baseline implementation

Earlier experimental code remains in the repository to demonstrate development progression but is not part of the final deployed system.

Architecture

Raspberry Pi (edge device) → Cloudinary (image storage)
Raspberry Pi (edge device) → Blynk Cloud → Mobile App

Design Decisions

A custom web dashboard was initially explored during development.
For the final release, the Blynk IoT platform was chosen to simplify deployment and provide a stable, mobile-friendly interface. This allowed the project to focus on core IoT concepts such as event handling, cloud integration, and remote monitoring rather than frontend development.

Release Level

This project corresponds to Release 3 on the grading spectrum, demonstrating a multi-component IoT system with cloud services, networking, and integrated device behaviour.





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
