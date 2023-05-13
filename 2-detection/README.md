# Assignment 2 - Detection

Follow the instructions in the [detection.ipynb](detection.ipynb) notebook.
This will clone both the 'yolov5' repo as well as this repo, install pip dependencies, and copy over the custom dataset configuration file.
This does require the "detection_assignment.zip" dataset, which for the sake of space is not included in this repo.

## detection_assignment.zip

This dataset was created from the provided "test.zip" and "train.zip" datasets. 
As the provided label format was not compatible with yolov5, we created a conversion script [convert.py](preparation/convert.py) to convert the labels to yolov5 format. 

We then split the training set into a training and validation set using text files "train.txt" and "val.txt" as described in the yolov5 documentation, 
which we generated using another simple script [split.py](preparation/split.py).