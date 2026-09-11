from Dataset_Builder.cleaner import clean_text_in_all
from loader import (label_all_dataset)
from cleaner import (clean_text_in_all)
#----Constant Values---------------
relevant_columns = ["text","label"]
H1_cat_labels = ["medical_emergency","other","survival"]
# Note: first one is the path we read from second one is the path we are saving to:
# Pair (1) : Loading dataset
origin_path_ES = r"C:\AI Stuff\AidCompanion-NLU\Dataset_Builder\Dataset_Raw\ES\H1"
JSON_path = r"C:\AI Stuff\AidCompanion-NLU\Dataset_Builder\JSON_Raw"
# Pair (2) Cleaning section
jsonl_path_ES = r"C:\AI Stuff\AidCompanion-NLU\Dataset_Builder\JSON_Raw\ES"
clean_path = r"C:\AI Stuff\AidCompanion-NLU\Dataset_Builder\Cleaned"

#----- Pipeline Phase (I)  ---------------------
#===Step 1: Load the raw datasets that we syntentically created into a single jsonl H1
label_all_dataset(origin_path_ES, JSON_path, relevant_columns,H1_cat_labels)

#===Step 2: Clean text in jsonl H1
clean_text_in_all(jsonl_path_ES,clean_path)

