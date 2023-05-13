#!/bin/python3
from __future__ import annotations

import os
from collections import namedtuple
from typing import Tuple
import argparse

Dota_line = namedtuple(
    "Dota", ["x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4", "category", "difficulty"])
Coco_line = namedtuple(
    "Coco", ["class_", "x_center", "y_center", "width", "height"])


def dota_to_coco(line: Dota_line, categories_to_class: dict[str, int], img_size: Tuple[int, int]) -> Coco_line:
    class_ = categories_to_class[line.category]

    min_x = int(min(line.x1, line.x2, line.x3, line.x4))
    max_x = int(max(line.x1, line.x2, line.x3, line.x4))
    min_y = int(min(line.y1, line.y2, line.y3, line.y4))
    max_y = int(max(line.y1, line.y2, line.y3, line.y4))

    width = max_x - min_x
    height = max_y - min_y

    x_center = min_x + width / 2
    y_center = min_y + height / 2

    # normalize
    x_center /= img_size[0]
    y_center /= img_size[1]
    width /= img_size[0]
    height /= img_size[1]

    c = Coco_line(class_, x_center, y_center, width, height)

    # if anything is negative, print a warning
    if x_center < 0 or y_center < 0 or width < 0 or height < 0:
        print(f"Warning: Negative value in {line}")
        print(c)

    return c


def main():
    parser = argparse.ArgumentParser(
        description="Convert DOTA labels to COCO labels")

    parser.add_argument("labels", help="The folder containing the DOTA labels")
    parser.add_argument("-o", "--output", help="The folder to output the COCO labels to",
                        dest="output", default="coco_labels")
    parser.add_argument("-s", "--size", help="The size of the images", dest="img_size",
                        nargs=2, type=int, default=(1024, 1024), metavar=("WIDTH", "HEIGHT"))

    args = parser.parse_args()

    labels_folder = args.labels
    output_labels_folder = args.output

    # width, height
    img_size = args.img_size

    # keep track of all categories and their class
    categories = set()

    # category string to class int
    category_to_class = {}

    print(f"Converting labels from {labels_folder} to {output_labels_folder}")

    # make the output folder if it doesn't exist
    os.makedirs(output_labels_folder, exist_ok=True)

    for file in os.listdir(labels_folder):
        # open the file and read the lines
        with open(os.path.join(labels_folder, file), "r") as f:
            lines = f.read().splitlines()

        # open the output file
        with open(os.path.join(output_labels_folder, file), "w") as f:
            for line in lines:
                *oobb, category, difficulty = line.split(" ")
                oobb = [float(x) for x in oobb]

                dota_line = Dota_line(*oobb, category, difficulty)

                if dota_line.category not in categories:
                    categories.add(dota_line.category)
                    category_to_class[dota_line.category] = len(categories) - 1

                coco_line = dota_to_coco(
                    dota_line, category_to_class, img_size)

                # write the coco line to the file
                f.write(
                    f"{coco_line.class_} {coco_line.x_center:.6f} {coco_line.y_center:.6f} {coco_line.width:.6f} {coco_line.height:.6f}\n")

    # print all categories with their class
    # print("Categories:")
    # for category, class_ in category_to_class.items():
    #     print(f" {class_}: \"{category}\"")


if __name__ == "__main__":
    main()
