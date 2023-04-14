import requests

from PIL import Image
from io import BytesIO

def load_image_by_pil(file_name, respect_exif=False):
    if isinstance(file_name, str):
        try:
            image = Image.open(file_name).convert('RGB')
        except:
            response = requests.get(file_name)
            image = Image.open(BytesIO(response.content)).convert('RGB')
    elif isinstance(file_name, bytes):
        import io
        image = Image.open(io.BytesIO(file_name)).convert('RGB')
    if respect_exif:
        from PIL import ImageOps
        image = ImageOps.exif_transpose(image)
    return image

