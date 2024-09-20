from PIL import Image
import imagehash
from typing import Tuple
from io import BytesIO



def generate_image_hashes(image_bytes:bytearray,image_size:Tuple[int,int]):
    print("generating image hashes")
    image = Image.open(BytesIO(image_bytes))
    # image = Image.frombytes(mode="RGB", size=image_size, data=image_bytes)
    print(image.size)
    p_hash = imagehash.phash(image)
    avg_hash = imagehash.average_hash(image)
    color_hash = imagehash.colorhash(image)
    d_hash = imagehash.dhash(image)
    w_hash = imagehash.whash(image)
    crop_hash = imagehash.crop_resistant_hash(image)
    return str(p_hash), str(avg_hash), str(color_hash), str(d_hash), str(w_hash), str(crop_hash)


