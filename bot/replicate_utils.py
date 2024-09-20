import replicate
import os
from dotenv import load_dotenv
from typing import Dict,List
load_dotenv()


def get_embedding(text: str,signed_image_url: str) -> Dict[str, List[float]]: 
    input = {"texts": text, "image_url": signed_image_url}
    results = replicate.run(
        "poipiii/jina-clip-v1:ae4b0d4877cc50d36589525ff741de8643f6265cdb564da91dff28a3bfad9f54",
        input=input
    )
    return results


