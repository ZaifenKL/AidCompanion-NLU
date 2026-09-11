import os
import json
import random

from Dataset_Builder.loader import out_path

#----Constant Values---------------
read_path = r"/Dataset_Builder/Merged\ES\hierarchy1_ES.jsonl"
out_path = r"C:\AI Stuff\AidCompanion-NLU\Dataset_Builder\Training"
train_name="hierarchy1_es_train"
val_name="hierarchy1_es_val"
test_name="hierarchy1_es_test"
train_ratio=0.7
val_ratio=0.15
test_ratio=0.15

#-----Functions--------------------
def split_jsonl(read_path, save_path, train_name, val_name, test_name,
                train_ratio=0.7, val_ratio=0.15, test_ratio=0.15):

    os.makedirs(save_path, exist_ok=True)

    # Read all the lines from the JSONL
    lines = []
    with open(read_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                lines.append(line)

    # Randomly mix
    random.shuffle(lines)

    total = len(lines)
    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)

    train_lines = lines[:train_end]
    val_lines = lines[train_end:val_end]
    test_lines = lines[val_end:]

    # Save the merged file
    current_folder = os.path.basename(os.path.dirname(read_path))
    os.makedirs(os.path.join(save_path, current_folder), exist_ok=True)
    out_path = os.path.join(save_path, current_folder)

    # Save the dataset
    train_path = os.path.join(out_path, f"{train_name}.jsonl")
    val_path = os.path.join(out_path, f"{val_name}.jsonl")
    test_path = os.path.join(out_path, f"{test_name}.jsonl")

    with open(train_path, "w", encoding="utf-8") as f:
        for line in train_lines:
            f.write(line + "\n")

    with open(val_path, "w", encoding="utf-8") as f:
        for line in val_lines:
            f.write(line + "\n")

    with open(test_path, "w", encoding="utf-8") as f:
        for line in test_lines:
            f.write(line + "\n")

    print(f"✔ Split completed:")
    print(f"  Train: {len(train_lines)} lines → {train_path}")
    print(f"  Val:   {len(val_lines)} lines → {val_path}")
    print(f"  Test:  {len(test_lines)} lines → {test_path}")

#-----Sequence-----------
if __name__ == "__main__":
    split_jsonl(read_path, out_path, train_name, val_name, test_name, train_ratio, val_ratio, test_ratio)