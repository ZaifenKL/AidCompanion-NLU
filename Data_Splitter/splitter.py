import os
import json
from pathlib import Path
import random
from datetime import datetime

#----Constant Values---------------
merged_path = r"C:/AI Stuff/AidCompanion-NLU/Dataset_Builder/Merged"
save_path = r"C:/AI Stuff/AidCompanion-NLU/Data_Splitter"
small_dataset_ratio = [0.90, 0.05, 0.05]

#-----Functions--------------------
def get_ratios(mode):
    #Returns train/val/test ratios based on mode:
    #A → 70/15/15
    #B → 80/20
    #C → user-defined

    mode = mode.lower()

    if mode == "a":
        return 0.70, 0.15, 0.15

    elif mode == "b":
        return 0.80, 0.00, 0.20

    elif mode == "c":
        print("\n🔧 Custom ratio mode selected.")
        train = float(input("Enter train ratio (0-1): "))
        val = float(input("Enter validation ratio (0-1): "))
        test = float(input("Enter test ratio (0-1): "))

        total = train + val + test
        if abs(total - 1.0) > 0.001:
            raise ValueError("❌ Ratios must sum to 1.0")

        return train, val, test

    else:
        raise ValueError("❌ Invalid mode. Use 'a', 'b', or 'c'.")

# ---------------------------------------------------------
# SPLIT SINGLE HIERARCHY
# ---------------------------------------------------------
def split_single_level(read_path, save_path, mode, report):
    """
    Splits a merged JSONL file into train/val/test automatically.
    """

    print(f"\n📌 Splitting level: {read_path}")

    # Detect ANY .jsonl file inside the hierarchy folder
    jsonl_files = [f for f in os.listdir(read_path) if f.endswith(".jsonl")]

    if not jsonl_files:
        print(f"⚠ No JSONL files found in {read_path}. Skipping.")
        return

    merged_file = os.path.join(read_path, jsonl_files[0])  # use first file

    if not os.path.exists(merged_file):
        print(f"⚠ No merged.jsonl found in {read_path}. Skipping.")
        return

    # Load merged file
    with open(merged_file, "r", encoding="utf-8") as f:
        lines = [json.loads(line) for line in f]

    total = len(lines)
    p = Path(read_path)
    hierarchy = p.name
    language = p.parent.name

    print(f"📊 Total examples: {total}")

    # ---------------------------------------------------------
    # APLICAR RATIO ESPECIAL AUTOMÁTICO PARA JERARQUÍAS PEQUEÑAS
    # ---------------------------------------------------------
    small_dataset = total < 120
    if small_dataset and mode.lower() != "c":
        print("⚠ WARNING: Small dataset detected (<120 examples).")
        print(f"   Applying special ratio: {small_dataset_ratio}")
        train_ratio, val_ratio, test_ratio = small_dataset_ratio
        warning = True
    else:
        train_ratio, val_ratio, test_ratio = get_ratios(mode)
        warning = False

    # Shuffle
    random.shuffle(lines)

    # Compute splits
    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)

    train_set = lines[:train_end]
    val_set = lines[train_end:val_end]
    test_set = lines[val_end:]

    # Output folder
    out_folder = os.path.join(save_path, language, hierarchy)
    os.makedirs(out_folder, exist_ok=True)

    # Save splits
    def write_jsonl(path, data):
        with open(path, "w", encoding="utf-8") as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

    write_jsonl(os.path.join(out_folder, "train.jsonl"), train_set)
    if val_ratio > 0:
        write_jsonl(os.path.join(out_folder, "val.jsonl"), val_set)
    write_jsonl(os.path.join(out_folder, "test.jsonl"), test_set)

    print(f"🎉 Split completed for {language}/{hierarchy}")
    print(f"   Train: {len(train_set)}")
    print(f"   Val:   {len(val_set)}")
    print(f"   Test:  {len(test_set)}\n")

    # Add to report
    report.append({
        "language": language,
        "hierarchy": hierarchy,
        "total": total,
        "train": len(train_set),
        "val": len(val_set),
        "test": len(test_set),
        "warning": warning
    })

# ---------------------------------------------------------
# AUTOMATIC SPLIT ALL DATASET ALL LANGUAGES ALL HIERARCHIES
# ---------------------------------------------------------
def split_all_levels(merged_path, save_path, mode, special_ratio= small_dataset_ratio):
    """
    Automatically splits all merged datasets:
    Merged/ES/H1 → Splits/ES/H1/train/val/test
    """

    print("\n🔍 Starting split_all_levels")

    report_data = []

    languages = [lang for lang in os.listdir(merged_path)
                 if os.path.isdir(os.path.join(merged_path, lang))]

    for language in languages:
        lang_path = os.path.join(merged_path, language)
        hierarchies = [h for h in os.listdir(lang_path)
                       if os.path.isdir(os.path.join(lang_path, h))]

        print(f"\n🌐 Language detected: {language}")
        print(f"   Hierarchies: {hierarchies}")

        for hierarchy in hierarchies:
            hierarchy_path = os.path.join(lang_path, hierarchy)
            split_single_level(hierarchy_path, save_path, mode, report_data)

#-----Sequence-----------
if __name__ == "__main__":

#===Step 5: split in test, validation and training sets
    split_all_levels(merged_path,save_path,mode="a",special_ratio=small_dataset_ratio)

   #Returns train/val/test ratios based on mode:
    #A → 70/15/15
    #B → 80/20
    #C → user-defined