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


# using a fixed mapping of categories to classes instead of growing the list when a new category is found
# this should keep the class numbers consistent
categories = [
    "small-vehicle",
    "large-vehicle",
    "bridge",
    "tennis-court",
    "ship",
    "harbor",
    "basketball-court",
    "soccer-ball-field",
    "swimming-pool"]


def dota_to_coco(line: Dota_line, img_size: Tuple[int, int]) -> Coco_line:
    # find the class number
    try:
        class_ = categories.index(line.category)
    except ValueError:
        # throw an error if the category is not found
        raise ValueError(f"Unknown category {line.category}")

    img_width, img_height = img_size

    min_x = int(min(line.x1, line.x2, line.x3, line.x4))
    max_x = int(max(line.x1, line.x2, line.x3, line.x4))
    min_y = int(min(line.y1, line.y2, line.y3, line.y4))
    max_y = int(max(line.y1, line.y2, line.y3, line.y4))

    bbox_width = max_x - min_x
    bbox_height = max_y - min_y

    x_center = min_x + bbox_width / 2
    y_center = min_y + bbox_height / 2

    # normalize
    x_center /= img_width
    y_center /= img_height
    bbox_width /= img_width
    bbox_height /= img_height

    c = Coco_line(class_, x_center, y_center, bbox_width, bbox_height)

    # if anything is negative, print a warning
    if x_center < 0 or y_center < 0 or bbox_width < 0 or bbox_height < 0:
        print(f"Warning: Negative value in {line}")
        print(c)

    return c


def main():
    parser = argparse.ArgumentParser(
        description="Convert DOTA labels to COCO labels")
    
    parser.add_argument("labels_dir", help="The folder containing the DOTA test labels")

    parser.add_argument("-o", "--output", help="The folder to output the COCO labels to",
                        dest="output")
    
    parser.add_argument("-s", "--size", help="The size of the images", dest="img_size",
                        nargs=2, type=int, default=(1024, 1024), metavar=("WIDTH", "HEIGHT"))

    args = parser.parse_args()
    

    # check if the labels folder exists
    if not os.path.isdir(args.labels_dir):
        raise ValueError(f"Labels directory {args.labels_dir} does not exist")
    
    # check if the output directory exists
    if os.path.isdir(args.output):
        raise ValueError(f"Output directory {args.output} already exists")

    
    # print a recap of the arguments, such as where the test and train labels are, where the output will be and the image size
    print("Summary:")
    print(f"  Labels: {args.labels_dir}")
    print(f"  Output: {args.output}")
    print(f"  Image size: {args.img_size[0]}x{args.img_size[1]}")


    # make the output folder if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    for file in os.listdir(args.labels_dir):
        # open the file and read the lines
        with open(os.path.join(args.labels_dir, file), "r") as f:
            lines = f.read().splitlines()

        # open the output file
        with open(os.path.join(args.output, file), "w") as f:
            for line in lines:
                *oobb, category, difficulty = line.split(" ")
                oobb = [float(x) for x in oobb]

                dota_line = Dota_line(*oobb, category, difficulty)

                if dota_line.category not in categories:
                    print(f"Warning: Unknown category {dota_line.category}")

                coco_line = dota_to_coco(
                    dota_line, (args.img_size[0], args.img_size[1]))

                # write the coco line to the file
                f.write(
                    f"{coco_line.class_} {coco_line.x_center:.6f} {coco_line.y_center:.6f} {coco_line.width:.6f} {coco_line.height:.6f}\n")

    # print all categories with their class
    print("names:")
    for i, category in enumerate(categories):
        print(f"  {i}: \"{category}\"")


if __name__ == "__main__":
    main()
