from flask import Flask, jsonify
from picamera2 import Picamera2
from upload_cloudinary import upload_image
import os

app = Flask(__name__)

picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()

IMAGE_PATH = "static/last_visitor.jpg"

@app.route("/take-photo")
def take_photo():
    picam2.capture_file(IMAGE_PATH)

    photo_url = upload_image(IMAGE_PATH)

    return jsonify({
        "photoUrl": photo_url
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
