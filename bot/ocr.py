from openai import AsyncOpenAI
from .prompts import OCR_PROMPT
import os
import base64
from PIL import Image
from dotenv import load_dotenv
import json
import io
import logging
import mimetypes

load_dotenv(override=True)

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
logger = logging.getLogger(__name__)


def compress_image(img_bytes: bytearray, img_type: str) -> bytes:
    img_type = img_type.split("/")[-1]
    img = Image.open(io.BytesIO(img_bytes))
    img_io = io.BytesIO()
    img.save(img_io, format=img_type, optimize=True, quality=50)
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
        return {"description": "Error analyzing image. Do you still want to report?"}
