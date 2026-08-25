import os
import pandas as pd
import re
import json

#----Constant Values---------------
dataset_raw = r"C:\AI Stuff\AidCompanion-NLU\Dataset_Builder\Dataset_Raw"
jsonl_path = r"C:\AI Stuff\AidCompanion-NLU\Dataset_Builder\JSON_Raw"
out_path = r"C:\AI Stuff\AidCompanion-NLU\Dataset_Builder\JSON_Cleaned"

#-----Functions---------------------
def clean_text(text):

    # Remove emojis
    # Eliminar emojis (versión más completa)
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticonos
        "\U0001F300-\U0001F5FF"  # símbolos y pictogramas
        "\U0001F680-\U0001F6FF"  # transporte y mapas
        "\U0001F700-\U0001F77F"  # alquimia
        "\U0001F780-\U0001F7FF"  # geometría
        "\U0001F800-\U0001F8FF"  # flechas suplementarias
        "\U0001F900-\U0001F9FF"  # símbolos suplementarios
        "\U0001FA00-\U0001FA6F"  # ajedrez y juegos
        "\U0001FA70-\U0001FAFF"  # objetos suplementarios
        "\U00002702-\U000027B0"  # dingbats
        "\U000024C2-\U0001F251"  # caracteres encerrados
        "]+",
        flags=re.UNICODE
    )
    text = emoji_pattern.sub(r'', text)

    # Remove punctuaction and multiple spaces
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r',+', ',', text)
    text = re.sub(r'\.{2,}', '.', text)
    text = re.sub(r':{2,}', '', text)

    # 3. Normalizar espacios antes de puntuación
    text = re.sub(r'\s+([,.!?])', r'\1', text)

    # 4. (Opcional) Eliminar puntuación no relevante
    text = re.sub(r'[^\w\s-]', '', text)

    text = text.lower().strip()

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