import json
from collections import Counter
import os
#----Constant Values---------------
merged_path_ES = r"/Dataset_Builder/Merged\ES\hierarchy1_ES.jsonl"

#-----Functions--------------------
def check_class_balance(jsonl_path):

    labels = []
    folder = os.path.basename(os.path.dirname(jsonl_path))

    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            if "label" in data:
                labels.append(data["label"])

    counts = Counter(labels)

    print(f"\n=== Class Balance {folder} :")
    total = sum(counts.values())

    for label, count in counts.items():
        pct = (count / total) * 100
        print(f" - {label}: {count} examples ({pct:.2f}%)")

    print(f"\nTotal examples {folder}: {total}")

#-----Sequence-----------
if __name__ == "__main__":
    check_class_balance(merged_path_ES)