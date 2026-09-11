from loader import (label_all_dataset)
#----Constant Values---------------
dataset_raw = r"C:\AI Stuff\AidCompanion-NLU\Dataset_Builder\Dataset_Raw"
out_path = r"C:\AI Stuff\AidCompanion-NLU\Dataset_Builder\JSON_Raw_New"
relevant_columns = ["text","label"]
#-----Functions---------------------
#Load the raw datasets that we syntentically created into a single clean jsonl
label_all_dataset(dataset_raw, out_path, relevant_columns)
