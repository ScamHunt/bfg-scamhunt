from openai import AsyncOpenAI
from .prompts import OCR_PROMPT
import os
import base64
from PIL import Image
from dotenv import load_dotenv
import json


load_dotenv(override=True)

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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
        print(e)
        return {"description": "Error analyzing image, do still want to report?"}
    result = json.loads(response.choices[0].message.content)
    return result
