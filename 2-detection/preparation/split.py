import random


file = "train/images/filename.txt"

train_val_split = 0.8

# open the file, read all lines, and split them into train and val files
with open(file, "r") as f:
    lines = f.read().splitlines()

# shuffle the lines
random.shuffle(lines)

# split the lines into train and val
train_lines = lines[:int(len(lines) * train_val_split)]
val_lines = lines[int(len(lines) * train_val_split):]

# write the train lines to the train file
with open("train.txt", "w") as f:
    for line in train_lines:
        f.write(f"{line}\n")
    
# write the val lines to the val file
with open("val.txt", "w") as f:
    for line in val_lines:
        f.write(f"{line}\n")
