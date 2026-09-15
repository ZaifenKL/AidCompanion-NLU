import os
import json
from pathlib import Path
#----Constant Values---------------
clean_json_path = r"C:\AI Stuff\AidCompanion-NLU\Dataset_Builder\Cleaned"
ouput_path = r"C:\AI Stuff\AidCompanion-NLU\Dataset_Builder\Merged"
#-----Functions---------------------
def merge_all_levels(read_path, save_path):

    print(f"\n🔍 Starting merge_all_levels in: {read_path}")

    # Detect languages (ES, EN)
    languages = [folder for folder in os.listdir(read_path)
                 if os.path.isdir(os.path.join(read_path, folder))]

    print(f"📁 Languages detected: {languages}\n")

    for language in languages:
        language_path = os.path.join(read_path, language)

        print(f"🌐 Processing language: {language}")

        # Detect hierarchies inside ES or EN
        hierarchies = [folder for folder in os.listdir(language_path)
                       if os.path.isdir(os.path.join(language_path, folder))]

        print(f"   📂 Hierarchies found: {hierarchies}")

        for hierarchy in hierarchies:
            hierarchy_path = os.path.join(language_path, hierarchy)
            output_name = f"{language}_{hierarchy}"

            print(f"\n   🔎 Merging hierarchy: {hierarchy}")
            merge_jsonl_single_level(hierarchy_path, save_path, output_name, language)


def merge_jsonl_single_level(read_path, save_path, output_name, language):

    print(f"📌 merge_jsonl_single_level called for: {read_path}")

    merged_lines = []
    files_found = []

    for root, dirs, files in os.walk(read_path):
        for file in files:
            if file.endswith(".jsonl"):
                full_path = os.path.join(root, file)
                files_found.append(full_path)
                print(f"   ✔ Found JSONL file: {full_path}")

                with open(full_path, "r", encoding="utf-8") as reader:
                    for line in reader:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            data = json.loads(line)
                            merged_lines.append(json.dumps(data, ensure_ascii=False))
                        except:
                            print(f"   ⚠ Corrupt line ignored in {full_path}")
                            continue

    if not files_found:
        print(f"⚠ No JSONL files found inside {read_path}. Skipping.\n")
        return

    # Detect hierarchy from read_path
    hierarchy = Path(read_path).name

    # Build output folder: save_path / ES / H1
    out_folder = os.path.join(save_path, language, hierarchy)
    os.makedirs(out_folder, exist_ok=True)

    out_file = os.path.join(out_folder, f"{output_name}.jsonl")

    print(f"💾 Saving merged file to: {out_file}")

    with open(out_file, "w", encoding="utf-8") as writer:
        for line in merged_lines:
            writer.write(line + "\n")

    print(f"🎉 Successfully merged {len(files_found)} files into {out_file}\n")

#-----Sequence-----------
if __name__ == "__main__":

    merge_all_levels(clean_json_path, ouput_path)
