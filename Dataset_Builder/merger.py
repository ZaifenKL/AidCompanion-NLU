import os
import csv
import re
import pandas as pd
import json
#----Constant Values---------------
clean_json_path = r"C:\AI Stuff\AidCompanion-NLU\Dataset_Builder\JSON_Cleaned"
ouput_path = r"C:\AI Stuff\AidCompanion-NLU\Dataset_Builder\Merged_Dataset"
merged_es = "hierarchy1_ES"

#-----Functions---------------------
def merge_jsonl(read_path, save_path, output_name):
    os.makedirs(save_path, exist_ok=True)

    merged_lines = []

    # Go through all the files in the folder
    for root, dirs, files in os.walk(read_path):
        for file in files:
            if file.endswith(".jsonl"):
                full_path = os.path.join(root, file)

                with open(full_path, "r", encoding="utf-8") as reader:
                    for line in reader:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            data = json.loads(line)
                            merged_lines.append(json.dumps(data, ensure_ascii=False))
                        except:
                            # Ignorar líneas corruptas
                            continue

                print(f"✔ Procesado: {full_path}")

            # Save the merged file
            current_folder = os.path.basename(root)
            os.makedirs(os.path.join(save_path, current_folder), exist_ok=True)
            out_path = os.path.join(save_path, current_folder)

    out_file = os.path.join(out_path, f"{output_name}.jsonl")
    with open(out_file, "w", encoding="utf-8") as writer:
        for line in merged_lines:
            writer.write(line + "\n")

    print(f"\n ===Successfully merged : {out_file}")

#-----Sequence-----------
if __name__ == "__main__":
    merge_jsonl(clean_json_path, ouput_path, merged_es)
