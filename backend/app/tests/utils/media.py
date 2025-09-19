import io

from fastapi import UploadFile

def create_fake_media():
    fake_png = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
    file = io.BytesIO(fake_png)
    file = UploadFile(filename="photo.png", file=file)
    return file