import os
import csv
import re
import pandas as pd
#----Constant Values---------------
dataset_raw = r"C:\AI Stuff\AidCompanion-NLU\Dataset_Builder\Dataset_Raw"
out_path = r"C:\AI Stuff\AidCompanion-NLU\Dataset_Builder\Dataset_Processed"

#-----Functions---------------------
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

def label_all_dataset(read_path,save_path):

    for root, dirs, files in os.walk(read_path):
        for file in files:
            if file.endswith(".csv") or file.endswith(".txt"):

                #Full path to the file
                full_path = os.path.join(root, file)

                #Automatically extract the filename and use the label
                base_name = re.sub(r'(?<!^)(?=[A-Z])', '_',file)
                base_name = base_name.lower()

                base_name = base_name.replace("dataset_", "")
                base_name = base_name.replace(".csv","")
                base_name = base_name.replace(".txt","_")

                #Now add the label to all the dataset
                df = add_label_to_dataset(full_path,base_name)
                #Convert to json and save
                out_path = os.path.join(save_path,dirs,f"{base_name}.jsonl")
                df.to_json(out_path,encoding='utf-8')

#-----Sequence-----------
if __name__ == "__main__":
    label_all_dataset(dataset_raw,out_path)