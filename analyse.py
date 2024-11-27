import argparse
import json
import os
from pathlib import Path


scam_threshold = 85


def analyse_results(dataset, results, output):
    with open(dataset, "r") as f:
        dataset = json.load(f)

    analysis = {}
    true_positives = 0
    false_positives = 0
    false_negatives = 0

    # Initialize the analysis dictionary
    for item in dataset:
        image_path = item["image"]
        scam_cats = item.get("scam_categories", [])
        categories = {scam_type: 0 for scam_type in scam_cats}
        obj = {"scam_detected": 0, "scam_categories": categories}
        analysis[image_path] = obj

    for file in os.listdir(results):
        with open(os.path.join(results, file), "r") as f:
            iteration = json.load(f)

        for item in dataset:
            img_path = item["image"]
            res = iteration["results"][img_path]
            is_scam = item["is_scam"]
            detected_as_scam = res["scam_likelihood"] >= scam_threshold

            if detected_as_scam and is_scam:
                true_positives += 1
                analysis[img_path]["scam_detected"] += 1
            elif detected_as_scam and not is_scam:
                false_positives += 1
            elif not detected_as_scam and is_scam:
                false_negatives += 1

            for scam_type in iteration["results"][img_path]["scam_types"]:
                scam_str = scam_type["scam_type"]
                if scam_str in analysis[img_path]["scam_categories"]:
                    analysis[img_path]["scam_categories"][scam_str] += 1

    # Add metrics to the analysis output
    analysis["metrics"] = {
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives
    }

    # Write the analysis results to the output file
    with open(output, "w") as f:
        json.dump(analysis, f, indent=2)

    return (true_positives, false_positives, false_negatives)


def calculate_f1_score(metrics):
    true_positives = metrics[0]
    false_positives = metrics[1]
    false_negatives = metrics[2]

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return f1_score


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run benchmark with specified parameters."
    )
    parser.add_argument(
        "--dataset",
        type=str,
        required=False,
        help="Path to the dataset JSON file.",
        default="benchmark/dataset.json",
    )
    parser.add_argument(
        "--results",
        type=str,
        required=False,
        help="Path to the results directory.",
        default="benchmark/results",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=False,
        help="Directory to save output results.",
        default="benchmark/analysis.json",
    )

    args = parser.parse_args()

    if not args.dataset.endswith(".json"):
        raise ValueError("The dataset file must have a .json extension.")

    metrics = analyse_results(args.dataset, args.results, args.output)
    print("Analysis complete.")
    f1_score = calculate_f1_score(metrics)
    print(f"F1 score: {f1_score}")
