import cloudinary
import cloudinary.uploader
import time

cloudinary.config(
    cloud_name="dpzvpt5f1",
    api_key="456774219243531",
    api_secret="E-K2ZKhm4Kd2WqznBz8V3q43-kQ",
)

def upload_image(image_path):
    result = cloudinary.uploader.upload(
        image_path,
        folder="dogsense",
        public_id="last_visitor",
        overwrite=True,
        invalidate=True
    )

    return result["secure_url"] + "?t=" + str(int(time.time()))
