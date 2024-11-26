import json
import os
from .benchmark import config


scam_threshold = 85


def analyse_results():
    with open(config["dataset_path"], "r") as f:
        dataset = json.load(f)

    with open("analysis.json", "w") as f:
        analysis = {}
        for item in dataset:
            analysis[item.image]["scam_detected"] = 0
            for scam_type in item["scam_categories"]:
                analysis[item.image]["scam_categories"][scam_type] = 0


        for file in os.listdir(config["output_path"]):
            with open(os.path.join(config["output_path"], file), "r") as f:
                iteration = json.load(f)
                
            for item in dataset:
                img_path = item["image"]
                res = iteration[img_path]
                scam_detected = analysis[img_path]["scam_detected"]
                if res["scam_likelihood"] >= 85:
                    analysis[img_path]["scam_detected"] += 1

                for scam_type in iteration[img_path]["scam_types"]:
                    scam_str = scam_type["scam_type"]
                    # check if scam_str in analysis and increment if it is

                

