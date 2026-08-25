import os
import csv
import re
import pandas as pd
#----Constant Values---------------
dataset_raw = r"C:\AI Stuff\AidCompanion-NLU\Dataset_Builder\Dataset_Raw"
out_path = r"C:\AI Stuff\AidCompanion-NLU\Dataset_Builder\JSON_Raw"
relevant_columns = ["text","label"]

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

def label_all_dataset(read_path,save_path,relevant_columns):

    os.makedirs(save_path, exist_ok=True)

    for root, dirs, files in os.walk(read_path):
        for file in files:
            if file.endswith(".csv") :

                #Full path to the file
                full_path = os.path.join(root, file)

                #Automatically extract the filename and use the label
                if file.endswith(".csv"):
                    base_name = file.replace(".csv","")

                base_name = base_name.replace("Dataset_","")

                base_name = re.sub(r'(?<!^)(?=[A-Z])', '_',base_name)
                base_name = base_name.lower()

                #Now add the label to all the dataset
                df = add_label_to_dataset(full_path,base_name)

                #Convert to json and save
                current_folder = os.path.basename(root)
                out_path = os.path.join(save_path,current_folder)

                # Make sure that the folder exists
                os.makedirs(out_path, exist_ok=True)

                out_path = os.path.join(out_path, f"{base_name}.jsonl")
                df = df[relevant_columns]
                df.to_json(out_path, orient="records", lines=True, force_ascii=False)


#-----Sequence-----------
if __name__ == "__main__":
    #Renamed column "usuario_input" to "text"
    rename_column_in_all(dataset_raw,"usuario_input","text")
    #Added "text" to relevant columns to create clean and simple jsonl
    label_all_dataset(dataset_raw,out_path,relevant_columns)



