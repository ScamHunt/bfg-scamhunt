import asyncio
import json
import time
import os
from ..bot.openai.ocr import ocr_image, Screenshot


config = {
    "iterations": 10,
    "dataset_path": "dataset.json",
    "output_path": "results",
}


async def benchmark():
    with open(config["dataset_path"], "r") as f:
        dataset = json.load(f)

    for i in range(config["iterations"]):
        start_time = time.time()
        results = {
            "results": await run_iteration(dataset),
            "iteration": i,
            "time": time.time() - start_time,
        }
        os.makedirs(config["output_path"])
        with open(f"{config["output_path"]}/iteration_{i+1}.json", "w") as f:
            json.dump(results, f, indent=4)


async def run_iteration(dataset) -> list[dict]:
    results = {}
    for item in dataset:
        start_time = time.time()
        result = await process_item(item)
        result["time"] = time.time() - start_time
        results[item.image] = result
    return results


async def process_item(item):
    file_path: str = item["image"]
    with open(file_path, "rb") as f:
        image_bytes = f.read()
        screenshot = await ocr_image(image_bytes, file_path.split(".")[-1])
        return screenshot.__dict__


if __name__ == "__main__":
    asyncio.run(benchmark())
