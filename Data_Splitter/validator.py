import os
import json
from collections import Counter
from datetime import datetime

from Data_Splitter.splitter import save_path

#----Constant Values---------------
split_root_path = r"C:\AI Stuff\AidCompanion-NLU\Data_Splitter"
invalid_folder = ["Reports"]
#-----Functions--------------------
def validate_dataset(split_root_path,invalid_folder) :
    """
    Validates all datasets inside Data_Splitter/<LANG>/<HIERARCHY>/
    - Integrity check
    - Duplicate detection
    - Corrupted lines
    - Category distribution
    - Histogram distribution
    - Text length analysis
    - Recommendations
    - Final status
    - Multi-hierarchy support
    """

    print("\n🔍 Starting dataset validation...")

    # Iterate languages (ES, EN, etc. BUT IGNORE INVALID FOLDERS)
    languages = [
        lang for lang in os.listdir(split_root_path)
        if os.path.isdir(os.path.join(split_root_path, lang))
           and lang not in invalid_folder
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
                "distribution": {},
                "lengths": {},
                "warnings": [],
                "recommendations": []
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
                lengths = []

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
                        lengths.append(len(obj["text"].split()))

                # Save results
                report["files"][split_name] = {
                    "total": len(labels),
                    "duplicates": len(duplicates),
                    "corrupted": len(corrupted)
                }

                report["duplicates"][split_name] = duplicates
                report["corrupted"][split_name] = corrupted
                report["distribution"][split_name] = dict(Counter(labels))
                report["lengths"][split_name] = lengths

            # ---------------------------------------------------------
            # Generate Markdown report
            # ---------------------------------------------------------
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            report_folder = os.path.join(split_root_path, "Reports", lang, hierarchy)
            os.makedirs(report_folder, exist_ok=True)

            report_path = os.path.join(report_folder, f"{timestamp}_validator_report.md")

            with open(report_path, "w", encoding="utf-8") as md:

                # ---------------------------------------------------------
                # EXECUTIVE SUMMARY
                # ---------------------------------------------------------
                md.write(f"# Dataset Validation Report\n\n")
                md.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
                md.write(f"**Language:** {lang}\n")
                md.write(f"**Hierarchy:** {hierarchy}\n\n")

                total_duplicates = sum(report["files"][f]["duplicates"] for f in report["files"])
                total_corrupted = sum(report["files"][f]["corrupted"] for f in report["files"])

                md.write("## Summary\n")
                md.write(f"- Total duplicates: **{total_duplicates}**\n")
                md.write(f"- Total corrupted lines: **{total_corrupted}**\n")

                # Determine dataset status
                if total_corrupted == 0 and total_duplicates < 5:
                    status = "READY FOR TRAINING"
                else:
                    status = "NEEDS FIXES"

                md.write(f"- Dataset Status: **{status}**\n\n")
                md.write("---\n\n")

                # ---------------------------------------------------------
                # PER SPLIT DETAILS
                # ---------------------------------------------------------
                for split_name, stats in report["files"].items():
                    md.write(f"## {split_name.upper()}\n")
                    md.write(f"- Total examples: {stats['total']}\n")
                    md.write(f"- Duplicates: {stats['duplicates']}\n")
                    md.write(f"- Corrupted lines: {stats['corrupted']}\n\n")

                    # ---------------------------------------------------------
                    # CATEGORY DISTRIBUTION + HISTOGRAM
                    # ---------------------------------------------------------
                    md.write("### Category Distribution\n")
                    md.write("| Category | Count | Histogram |\n")
                    md.write("|----------|-------|-----------|\n")

                    dist = report["distribution"][split_name]
                    max_count = max(dist.values()) if dist else 1

                    for label, count in dist.items():
                        bar = "█" * int((count / max_count) * 20)
                        md.write(f"| {label} | {count} | {bar} |\n")

                    md.write("\n")

                    # ---------------------------------------------------------
                    # BALANCE ANALYSIS PER SPLIT
                    # ---------------------------------------------------------
                    md.write("## Balance Analysis\n\n")

                    for split_name, dist in report["distribution"].items():

                        md.write(f"### {split_name.upper()}\n")

                        if not dist:
                            md.write("- No data available.\n\n")
                            continue

                        # Largest and smallest classes
                        largest_label = max(dist, key=dist.get)
                        smallest_label = min(dist, key=dist.get)
                        largest_count = dist[largest_label]
                        smallest_count = dist[smallest_label]

                        ratio = largest_count / max(smallest_count, 1)

                        # Determine balance status
                        if ratio <= 1.5:
                            balance_status = "🟢 Good balance"
                        elif ratio <= 3:
                            balance_status = "🟡 Moderate imbalance"
                        else:
                            balance_status = "🔴 Strong imbalance"

                        md.write(f"- Largest category: **{largest_label}** ({largest_count})\n")
                        md.write(f"- Smallest category: **{smallest_label}** ({smallest_count})\n")
                        md.write(f"- Ratio largest/smallest: **{ratio:.2f}**\n")
                        md.write(f"- Balance status: **{balance_status}**\n\n")

                        # Recommendations
                        if ratio > 3:
                            md.write(f"- Recommendation: Add more samples for **{smallest_label}**.\n")
                        elif ratio > 1.5:
                            md.write(f"- Recommendation: Consider adding examples for **{smallest_label}**.\n")
                        else:
                            md.write("- Balance looks good.\n")

                        md.write("\n---\n\n")

                    # ---------------------------------------------------------
                    # TEXT LENGTH ANALYSIS
                    # ---------------------------------------------------------
                    lengths = report["lengths"][split_name]
                    if lengths:
                        avg_len = sum(lengths) / len(lengths)
                        md.write("### Text Length Analysis\n")
                        md.write(f"- Average length: {avg_len:.2f} tokens\n")
                        md.write(f"- Min length: {min(lengths)} tokens\n")
                        md.write(f"- Max length: {max(lengths)} tokens\n\n")

                    md.write("---\n\n")

                # ---------------------------------------------------------
                # WARNINGS: categories only in val/test
                # ---------------------------------------------------------
                md.write("## Warnings\n")

                train_labels = set(report["distribution"]["train"].keys())
                val_labels = set(report["distribution"]["val"].keys())
                test_labels = set(report["distribution"]["test"].keys())

                only_in_val = val_labels - train_labels
                only_in_test = test_labels - train_labels

                if only_in_val:
                    md.write(f"- ⚠ Categories only in **val**: {list(only_in_val)}\n")
                if only_in_test:
                    md.write(f"- ⚠ Categories only in **test**: {list(only_in_test)}\n")
                if not only_in_val and not only_in_test:
                    md.write("- No category distribution warnings.\n")

                md.write("\n---\n\n")

                # ---------------------------------------------------------
                # RECOMMENDATIONS
                # ---------------------------------------------------------
                md.write("## Recommendations\n")

                # Small classes
                for split_name, dist in report["distribution"].items():
                    for label, count in dist.items():
                        if count < 30:
                            md.write(f"- Add more examples for category **{label}** ({count} samples in {split_name}).\n")

                if total_duplicates > 0:
                    md.write(f"- Remove or review {total_duplicates} duplicated examples.\n")

                if total_corrupted > 0:
                    md.write(f"- Fix {total_corrupted} corrupted lines.\n")

                md.write("\n---\n\n")

                # ---------------------------------------------------------
                # FINAL STATUS
                # ---------------------------------------------------------
                md.write("## Final Status\n")
                md.write(f"**{status}**\n")

            print(f"📄 Validation report saved at: {report_path}")

#-----Sequence-----------
if __name__ == "__main__":
    validate_dataset(split_root_path,invalid_folder)
