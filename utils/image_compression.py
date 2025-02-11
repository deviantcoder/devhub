import os

from PIL import Image
from io import BytesIO
from django.core.files import File


def compress_image(file):
    with Image.open(file) as img:
        if img.mode in ('P', 'RGBA'):
            img = img.convert('RGB')

        img_io = BytesIO()

        img.save(img_io, format='JPEG', quality=50, optimize=True)
        img_io.seek(0)

        return File(img_io, name=file.name)