import json
import os
from .benchmark import config


# def analyse_results():
#     with open(config["dataset_path"], "r") as f:
#         dataset = json.load(f)

    # with open("analysis.json", "w") as f:
    #     for item in dataset:
    #         for file in os.listdir(config["output_path"]):
    #             with open(os.path.join(config["output_path"], file), "r") as f:
    #                 iteration = json.load(f)
    #                 if iteration["iteration"] == item["iteration"]:
