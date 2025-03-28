import asyncio
import json
import mimetypes
import time
import os
import argparse
import sys
from pathlib import Path
from analyse import analyse_results

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from bot.openai.ocr import ocr_image, Screenshot

async def benchmark(iterations, dataset_path, output_path, images):
    with open(dataset_path, "r") as f:
        dataset = json.load(f)

    # Validate images before running the benchmark
    validate_images(dataset)
    print(f"Validated {len(dataset)} images.")
    
    for i in range(iterations):
        print(f"Running iteration {i+1} of {iterations}...")
        start_time = time.time()
        results = {
            "results": await run_iteration(dataset, images),
            "iteration": i,
            "time": time.time() - start_time,
        }
        os.makedirs(output_path, exist_ok=True)
        with open(f"{output_path}/iteration_{i+1}.json", "w", ) as f:
            json.dump(results, f, indent=4)


def validate_images(dataset):
    for item in dataset:
        file_path = f"benchmark/images/{item['image']}.jpg"
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Image file not found: {file_path}")
        file_mimetype = mimetypes.guess_type(file_path)
        if file_mimetype[0] != "image/jpeg":
            raise ValueError(f"Image file is not a JPEG: {file_path}")


async def run_iteration(dataset, images) -> list[dict]:
    results = {}
    for item in dataset:
        if images and item["image"] not in images:
            continue
        start_time = time.time()
        result = await process_item(item)
        result["time"] = time.time() - start_time
        results[item["image"]] = result
    return results


async def process_item(item):
    file: str = item["image"]
    with open(f"benchmark/images/{file}.jpg", "rb") as f:
        try:
            print(f"Processing item {file}...")
            image_bytes = f.read()
            file_mimetype = mimetypes.guess_type(f.name)
            screenshot = await ocr_image(image_bytes, file_mimetype[0], compress=False)
            
            # Convert Screenshot object to dict
            screenshot_dict = screenshot.__dict__
            
            # Convert ScamType objects to dicts
            screenshot_dict['scam_types'] = [
                {'scam_type': st.scam_type, 'score': st.score}
                for st in screenshot_dict['scam_types']
            ]
            
            return screenshot_dict
        except Exception as e:
            print(f"Error processing item {item['image']}: {e}")
            return {"error": str(e)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run benchmark with specified parameters."
    )
    parser.add_argument(
        "--iterations",
        type=int,
        required=False,
        help="Number of iterations to run.",
        default=5,
    )
    parser.add_argument(
        "--dataset",
        type=str,
        required=False,
        help="Path to the dataset JSON file.",
        default="benchmark/dataset.json",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=False,
        help="Directory to save output results.",
        default="benchmark/results",
    )
    parser.add_argument(
        "--images",
        type=str,
        nargs="+",  # This allows for multiple values
        required=False,
        # default=["3", "4"],
        help="List of image names to process.",
    )

    args = parser.parse_args()

    # Validate the number of iterations
    if args.iterations <= 0:
        raise ValueError("The number of iterations must be greater than 0.")

    # Validate the dataset file
    if not args.dataset.endswith(".json"):
        raise ValueError("The dataset file must have a .json extension.")

    # Validate the output path
    output_path = Path(args.output)
    if not output_path.is_dir() and not output_path.parent.is_dir():
        raise ValueError(f"The output path is not valid: {args.output}")

    # Create the output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)

    asyncio.run(benchmark(args.iterations, args.dataset, args.output, args.images))
