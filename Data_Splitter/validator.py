import os
import json
from collections import Counter
from datetime import datetime

from Data_Splitter.splitter import save_path

#----Constant Values---------------
split_root_path = r"C:\AI Stuff\AidCompanion-NLU\Data_Splitter"
#-----Functions--------------------
def validate_dataset(split_root_path):
    """
    Validates all datasets inside Data_Splitter/<LANG>/<HIERARCHY>/
    - Integrity check
    - Duplicate detection
    - Corrupted lines
    - Category distribution
    - Multi-hierarchy support
    - Markdown report per hierarchy
    """

    print("\n🔍 Starting dataset validation...")

    # Iterate languages (ES, EN, etc.)
    languages = [
        lang for lang in os.listdir(split_root_path)
        if os.path.isdir(os.path.join(split_root_path, lang))
    ]

    for lang in languages:
        lang_path = os.path.join(split_root_path, lang)

        # Iterate hierarchies (H1, H2, H3...)
        hierarchies = [
            h for h in os.listdir(lang_path)
            if os.path.isdir(os.path.join(lang_path, h))
        ]

        for hierarchy in hierarchies:
            hierarchy_path = os.path.join(lang_path, hierarchy)

            print(f"\n🌐 Validating {lang}/{hierarchy}")

            # Files to validate
            files = {
                "train": os.path.join(hierarchy_path, "train.jsonl"),
                "val": os.path.join(hierarchy_path, "val.jsonl"),
                "test": os.path.join(hierarchy_path, "test.jsonl")
            }

            # Storage for report
            report = {
                "language": lang,
                "hierarchy": hierarchy,
                "files": {},
                "duplicates": {},
                "corrupted": {},
                "distribution": {}
            }

            # Validate each split file
            for split_name, file_path in files.items():

                if not os.path.exists(file_path):
                    print(f"⚠ Missing file: {file_path}")
                    continue

                print(f"   📄 Checking {split_name}.jsonl")

                seen = set()
                duplicates = []
                corrupted = []
                labels = []

                with open(file_path, "r", encoding="utf-8") as f:
                    for line_number, line in enumerate(f, start=1):
                        try:
                            obj = json.loads(line)
                        except:
                            corrupted.append(line_number)
                            continue

                        # Check required fields
                        if "text" not in obj or "label" not in obj:
                            corrupted.append(line_number)
                            continue

                        # Detect duplicates
                        key = (obj["text"], obj["label"])
                        if key in seen:
                            duplicates.append(line_number)
                        else:
                            seen.add(key)

                        labels.append(obj["label"])

                # Save results
                report["files"][split_name] = {
                    "total": len(labels),
                    "duplicates": len(duplicates),
                    "corrupted": len(corrupted)
                }

                report["duplicates"][split_name] = duplicates
                report["corrupted"][split_name] = corrupted
                report["distribution"][split_name] = dict(Counter(labels))

            # ---------------------------------------------------------
            # Generate Markdown report
            # ---------------------------------------------------------
            report_folder = os.path.join(split_root_path, "Reports", lang, hierarchy)
            os.makedirs(report_folder, exist_ok=True)

            report_path = os.path.join(report_folder, "validator_report.md")

            with open(report_path, "w", encoding="utf-8") as md:

                md.write(f"# Dataset Validation Report\n\n")
                md.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
                md.write(f"**Language:** {lang}\n")
                md.write(f"**Hierarchy:** {hierarchy}\n\n")
                md.write("---\n\n")

                # Per split file
                for split_name, stats in report["files"].items():
                    md.write(f"## {split_name.upper()}\n")
                    md.write(f"- Total examples: {stats['total']}\n")
                    md.write(f"- Duplicates: {stats['duplicates']}\n")
                    md.write(f"- Corrupted lines: {stats['corrupted']}\n\n")

                    md.write("### Category Distribution\n")
                    md.write("| Category | Count |\n")
                    md.write("|----------|-------|\n")
                    for label, count in report["distribution"][split_name].items():
                        md.write(f"| {label} | {count} |\n")
                    md.write("\n---\n\n")

                md.write("\n\n")

            print(f"📄 Validation report saved at: {report_path}")

#-----Sequence-----------
if __name__ == "__main__":
    validate_dataset(split_root_path)
