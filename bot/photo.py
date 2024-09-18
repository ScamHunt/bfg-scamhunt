from telegram import Update, PhotoSize, File
from typing import List
import base64
from .openai import extract_image

def handle_photo(photos: List[PhotoSize]):
    """Handle incoming photo."""
    file = await photo[-1].get_file()
    byte_arr = await file.download_as_bytearray()
    b64 = base64.b64encode(byte_arr)
    response = extract_image(b64)
    return response
