import os
import csv
from pathlib import Path
import pandas as pd
#----Constant Values---------------
read_path = r"C:\AI Stuff\AidCompanion-NLU\Dataset_Builder\Dataset_Raw\ES\H1"
out_path = r"C:\AI Stuff\AidCompanion-NLU\Dataset_Builder\JSON_Raw"
relevant_columns = ["text","label"]
first_cat_labels = ["medical_emergency","other","survival"]

#-----Functions---------------------

def rename_column(path, old_name, new_name):
    #Rename a column in a df
    # Detect extension
    ext = os.path.splitext(path)[1].lower()
    file = os.path.basename(path)

    # Load type
    if ext == ".csv":
        df = pd.read_csv(path)
    elif ext == ".jsonl":
        df = pd.read_json(path, lines=True)
    else:
        print(f"⚠ {file} Not supported format: {ext}")
        return

    # Verify that the column exists
    if old_name not in df.columns:
        print(f"⚠ Column '{old_name}' does not exist in: {file}")

    else:
        # Rename if it exists
        df = df.rename(columns={old_name: new_name})

        # Save the same format
        if ext == ".csv":
            df.to_csv(path, index=False)

        elif ext == ".jsonl":
            df.to_json(path, orient="records", lines=True, force_ascii=False)

        print(f"✔ Column '{old_name}' renamed to '{new_name}' at: {path}")


def rename_column_in_all(path, old_name, new_name):
    # Rename variable column in a group of files in path
    for root, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)
            rename_column(full_path,  old_name,new_name)

    print("=== Finished")

def add_label_to_dataset(path,label):
    # 1. Detect delimiter
    with open(path, 'r', encoding='utf-8') as f:
        dialect = csv.Sniffer().sniff(f.read(2048))
        sep = dialect.delimiter

    # 2. Load file with delimiter
    df = pd.read_csv(path, sep=sep)

    # 3. Add label column
    df["label"]=label

    return df

def label_all_dataset(read_path, save_path, relevant_columns, labels):
    os.makedirs(save_path, exist_ok=True)

    # 1. Get csv files and alphabetic order
    files = [f for f in os.listdir(read_path) if f.endswith(".csv")]
    files.sort()

    # 2. Alphabetical orden of labels
    labels_sorted = sorted(labels)

    # 3. Validar que haya tantas etiquetas como archivos
    if len(files) != len(labels_sorted):
        raise ValueError(
            f"The number of labels ({len(labels_sorted)}) "
            f"does not match the number of files ({len(files)})."
        )

    # 4. Process every file with it's own label
    for idx, file in enumerate(files):
        full_path = os.path.join(read_path, file)
        label = labels_sorted[idx]

        # Detect csv delimiter
        with open(full_path, 'r', encoding='utf-8') as f:
            dialect = csv.Sniffer().sniff(f.read(2048))
            sep = dialect.delimiter

        df = pd.read_csv(full_path, sep=sep)

        # Assign label
        df["label"] = label

        # Filter relevant columns
        df = df[relevant_columns]

        # Detect language and hierarchy from the path
        p = Path(full_path)
        hierarchy = p.parent.name  # H1 or H2
        language = p.parent.parent.name  # ES or EN

        # Build output folder: save_path / language / hierarchy
        out_folder = os.path.join(save_path, language, hierarchy)
        os.makedirs(out_folder, exist_ok=True)

        # Final output file
        out_file = os.path.join(out_folder, f"{label}.jsonl")
        df.to_json(out_file, orient="records", lines=True, force_ascii=False)

        print(f"✔ Proccesing file: {file} → label'{label}' (alphabetic order)")


#-----Sequence-----------
if __name__ == "__main__":

    label_all_dataset(read_path,out_path,relevant_columns,first_cat_labels)



