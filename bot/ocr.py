from openai import AsyncOpenAI
from .prompts import OCR_PROMPT
import os
import base64
from PIL import Image
from dotenv import load_dotenv
import json



client = AsyncOpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)



def img_to_base64(img_bytes:bytearray):
    base64_str = base64.b64encode(img_bytes).decode("utf-8")
    return base64_str



async def ocr_image(image_bytes:bytearray, img_type:str) ->dict:
    print("converting image to base64")
    img_b64_str = img_to_base64(image_bytes)
    print("sending request to openai")
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content":[
            {"type":"text","text":OCR_PROMPT},
            {
                        "type": "image_url",
                        "image_url": {"url": f"data:{img_type};base64,{img_b64_str}"},
            },    
        ]}],



    response_format={ "type": "json_object" }
)
    print("response received from openai")

    result = json.loads(response.choices[0].message.content)

    return result







