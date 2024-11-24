from bot.openai.ocr import ocr_image
import mimetypes


async def is_image_scam(image):
    image_bytes = image.file.read()
    file_mimetype = mimetypes.guess_type(image.filename)[0]
    screenshot = await ocr_image(image_bytes, file_mimetype)
    return screenshot

def is_link_scam(link: str):
    # TODO: Add link scam check
    return {"is_scam": True}

def is_phone_scam(phone: str):
    # TODO: Add phone scam check
    return {"is_scam": True}
