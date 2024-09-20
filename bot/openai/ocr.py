from openai import AsyncOpenAI, BaseModel
from .prompts import OCR_PROMPT
import os
import base64
from PIL import Image
from dotenv import load_dotenv
import json
import logging


load_dotenv(override=True)

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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


async def ocr_image(image_bytes: bytearray, img_type: str) -> dict:
    img_b64_str = img_to_base64(image_bytes)
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
    except Exception as e:
        logging.error(e)
        return {"description": "Error analyzing image, do still want to report?"}
    result = json.loads(response.choices[0].message.content)
    return result
