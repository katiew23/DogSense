DogSense 

IoT Dog Activity Monitoring System

DogSense is an IoT-based monitoring system designed to detect and log activity in a home environment when a dog is left alone.
The system uses a Raspberry Pi with a camera and Sense HAT sensors to detect movement and physical disturbance, capture images, and publish events using MQTT. A backend service stores events for analysis, while a Blynk mobile app provides live feedback and manual control.

Project Aim

The aim of this project is to design and implement a working IoT prototype that:

Collects data from physical sensors

Applies local processing and decision-making

Communicates events using standard IoT networking protocols

Separates device logic from backend data handling

Presents live feedback through a lightweight user interface

System Architecture

High-level architecture:

Sensors (Camera + Sense HAT)
↓
Raspberry Pi Device (dogSense.py)
↓
MQTT Broker
↓
Backend Listener (SQLite + alert logic)
↓
Blynk Mobile App (live updates + manual control)

The architecture follows a message-driven IoT design where the device, messaging layer, backend processing, and user interface are clearly separated.

Hardware Used

Raspberry Pi

Raspberry Pi Camera Module

Sense HAT (accelerometer)

Sensors & Event Detection
Camera-Based Movement Detection

Periodic image capture

Image differencing used to detect movement

Significant changes trigger an event

An image is captured and uploaded on detection

Sense HAT Accelerometer (Shake Detection)

Raw accelerometer values are read from the Sense HAT

A calibrated threshold is used to detect sudden physical movement

This logic is based on the accelerometer exercise from Lecture 1 and tuned using real sensor data

Manual Capture (User Override)

A Blynk button allows the user to manually trigger an image capture

Demonstrates remote interaction with the IoT device via a cloud-based UI

Networking & IoT Technologies

MQTT
Lightweight messaging protocol used to publish activity events from the device to a backend service.

Blynk Cloud
Provides live UI feedback, manual control, and device status updates.

Cloudinary
Used to externally host captured images so they can be referenced across services.

Due to Blynk platform constraints, the image widget does not support dynamically changing image URLs at runtime. To address this, images are uploaded to a fixed Cloudinary URL, allowing the Blynk app to display the most recent image without requiring URL updates. Full image history can be accessed directly via Cloudinary.

Backend Service

The backend listener (backend_listener.py) subscribes to the MQTT topic and:

Stores events in a SQLite database

Records:

Device ID

Event type

Timestamp

Image URL

Implements derived behaviour by detecting bursts of activity and issuing alerts

This backend service is intentionally decoupled from the device logic to reflect real-world IoT system design.

MQTT Message Schema

{
"deviceId": "dogsense_pi_01",
"eventType": "camera_movement | device_shake | manual_capture",
"timestamp": "ISO-8601 timestamp",
"imageUrl": "https://cloudinary.com/
..."
}

User Interface

The primary user interface for the system is a Blynk mobile application, which provides:

Live event feedback

Visual status indicators

Manual capture functionality

A lightweight and responsive monitoring experience

During development, a web-based dashboard was also explored.
This approach was later intentionally removed in favour of a clearer IoT-focused architecture using MQTT and a lightweight mobile UI, reducing system complexity while maintaining full functionality.

Reliability & Design Considerations

Cooldown logic is implemented to prevent event flooding

Camera and accelerometer triggers operate independently

Short delays are intentionally included to ensure stable operation and network reliability

The system prioritises reliability and clarity over raw responsiveness

How to Run

Device (Raspberry Pi)
python3 dogSense.py

Backend Listener
python3 backend_listener.py

Ensure:

An MQTT broker is running locally

The Blynk authentication token is set as an environment variable

Project Status

This project represents a Release 3 (Excellent) IoT prototype, demonstrating:

Multi-sensor data collection

Event-driven device logic

Lightweight messaging with MQTT

Backend persistence and derived behaviour

Cloud-based UI integration

Author

Kate Williams
HDip Computer Science – IoT & Networking
