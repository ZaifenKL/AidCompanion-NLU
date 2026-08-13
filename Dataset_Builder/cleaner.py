import os
import pandas as pd
import re
import json

#----Constant Values---------------
dataset_raw = r"C:\AI Stuff\AidCompanion-NLU\Dataset_Builder\Dataset_Raw"
jsonl_path = r"C:\AI Stuff\AidCompanion-NLU\Dataset_Builder\JSON_Raw"
out_path = r"C:\AI Stuff\AidCompanion-NLU\Dataset_Builder\Dataset_Cleaned"

#-----Functions---------------------
def clean_text(text):
    # Remove leading/trailing spaces
    text = text.strip()

    # Replace multiple spaces with one
    text = re.sub(r'\s+', ' ', text)

    # Replace multiple commas with one
    text = re.sub(r',+', ',', text)

    # Remove spaces before punctuation
    text = re.sub(r'\s+([,.!?])', r'\1', text)

    #Remove consecutive or multiple dots replace with one
    text = re.sub(r'\.{2,}', '.', text)

    # Remove repeated colons (::, :::, etc.)
    text = re.sub(r':{2,}', '', text)

    text = re.sub(r'[\U00010000-\U0010ffff]', '', text)

    return text

def clean_text_in_all(read_path, save_path):

    os.makedirs(save_path, exist_ok=True)

    for root, dirs, files in os.walk(read_path):
        for file in files:
            if file.endswith(".jsonl"):

                full_path = os.path.join(root, file)

                cleaned_lines = []

                # Read line by line
                with open(full_path, "r", encoding="utf-8") as reader:
                    for line in reader:
                        if not line.strip():
                            continue

                        data = json.loads(line)

                        # Clean "text"
                        if "text" in data:
                            data["text"] = clean_text(data["text"])

                        cleaned_lines.append(json.dumps(data, ensure_ascii=False))

                # Convert to json and save
                current_folder = os.path.basename(root)
                os.makedirs(os.path.join(save_path, current_folder), exist_ok=True)

                out_path = os.path.join(save_path, current_folder, file)

                # Overwrite the jsonl file with the clean lines
                with open(out_path, "w", encoding="utf-8") as writer:
                    for line in cleaned_lines:
                        writer.write(line + "\n")

                print(f"✔ File cleaned and saved at: {out_path}")

#-----Sequence-----------
if __name__ == "__main__":
    clean_text_in_all(jsonl_path,out_path)