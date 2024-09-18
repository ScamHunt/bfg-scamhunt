from openai import OpenAI
import os

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.getenv("OPENAI_API_KEY"),
)

async def extract_image(b64_img):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What’s in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{b64_img}"
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content[0].text
