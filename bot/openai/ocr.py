from openai import AsyncOpenAI, BaseModel
from .prompts import OCR_PROMPT
import os
import base64
from PIL import Image
from dotenv import load_dotenv
import json
import logging

import io
import mimetypes

load_dotenv(override=True)

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
logger = logging.getLogger(__name__)


# class Screenshot(BaseModel):
#     username: str
#     group: str
#     text: str
#     description: str
#     links: list[str]
#     likes: str
#     comments: str
#     shares: str
#     location: str
#     platform: str
#     email: str
#     phone_extension: str
#     phone_number: str
#     ad_or_post: str
#     is_sponsored: str
#     scam_likelihood: int
#     platform: str


def img_to_base64(img_bytes: bytearray):
    base64_str = base64.b64encode(img_bytes).decode("utf-8")
    return base64_str


def compress_image(img_bytes: bytearray, img_type: str) -> bytes:
    img_type = img_type.split("/")[-1]
    img = Image.open(io.BytesIO(img_bytes))
    img_io = io.BytesIO()
    img.save("before.png", format=img_type)
    img.save(img_io, format=img_type, optimize=True, quality=50)
    img.save("after.png", format=img_type, optimize=True, quality=50)
    img_io.seek(0)
    return img_io.getvalue()


def img_to_base64(img_bytes: bytes) -> str:
    return base64.b64encode(img_bytes).decode("utf-8")


async def ocr_image(file) -> dict:
    file_mimetype = mimetypes.guess_type(file.file_path)
    image_bytes = await file.download_as_bytearray()
    img_type = file_mimetype[0]
    compressed_image = compress_image(image_bytes, img_type)
    img_b64_str = img_to_base64(compressed_image)
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": OCR_PROMPT},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{img_type};base64,{img_b64_str}"
                            },
                        },
                    ],
                }
            ],
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        logger.error(f"Error analyzing image: {e}")
        return {"description": "Error analyzing image, do still want to report?"}
    result = json.loads(response.choices[0].message.content)
    return result
