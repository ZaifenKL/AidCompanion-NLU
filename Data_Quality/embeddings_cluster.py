from sentence_transformers import SentenceTransformer
import json
import hashlib
import os
#----Constant Values---------------
json_merged_H1 = r"C:\AI Stuff\AidCompanion-NLU\Data_Builder\Merged\ES\H1"
model_name = "all-MiniLM-L6-v2"
output_path = r"C:\AI Stuff\AidCompanion-NLU\Data_Quality"
#-----Functions--------------------
def generate_embeddings_from_jsonl(jsonl_path, model_name="all-MiniLM-L6-v2"):
    """
    Load text from JSONL merged and generates embeddings using SentenceTransformers.
    Ideal para análisis de near-duplicates con DBSCAN.
    """

    # Step 1: load JSONL text
    texts = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line)
                if "text" in obj:
                    texts.append(obj["text"])
            except json.JSONDecodeError:
                # Línea corrupta, la ignoramos
                continue

    if not texts:
        raise ValueError("Could not find any text in the JSONL.")

    # Step 2: load embeddings model
    model = SentenceTransformer(model_name)

    # Step 3: generate embeddings
    embeddings = model.encode(texts, normalize_embeddings=True)

    return texts, embeddings


def save_embeddings_with_structure(
        texts,
        embeddings,
        source_jsonl_path,
        base_output_path):
    """
    Guarda un JSONL con id (hash), texto y embedding en una estructura de carpetas
    que replica la ruta original del archivo fuente.

    Ejemplo:
    Si source_jsonl_path = "C:\\AI Stuff\\AidCompanion-NLU\\Dataset_Raw\\ES\\H1\\merged.jsonl"

    Entonces guardará en:
    C:\\AI Stuff\\AidCompanion-NLU\\Data_Quality\\ES\\H1\\embeddings.jsonl
    """

    # 1. Extraer carpetas relativas después de Dataset_Raw o JSON_Raw
    parts = os.path.normpath(source_jsonl_path).split(os.sep)

    # Detectar el índice donde empieza la parte ES/H1
    # Buscamos carpetas típicas del proyecto
    keywords = ["Dataset_Raw", "JSON_Raw", "ES", "EN"]
    start_idx = None

    for i, p in enumerate(parts):
        if p in keywords:
            start_idx = i
            break

    if start_idx is None:
        raise ValueError("No se pudo detectar la estructura ES/H1 en la ruta del archivo fuente.")

    # Extraer la parte relativa (ej: ES/H1)
    relative_parts = parts[start_idx + 1: -1]  # omitimos el archivo final

    # 2. Construir la ruta destino replicando la estructura
    output_dir = os.path.join(base_output_path, *relative_parts)
    os.makedirs(output_dir, exist_ok=True)

    # 3. Nombre del archivo final
    output_file = os.path.join(output_dir, "embeddings.jsonl")

    # 4. Guardar JSONL
    with open(output_file, "w", encoding="utf-8") as f:
        for text, emb in zip(texts, embeddings):
            text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()

            record = {
                "id": text_hash,
                "text": text,
                "embedding": emb.tolist()
            }

            f.write(json.dumps(record) + "\n")

    return output_file


#-----Sequence-----------
if __name__ == "__main__":
    texts_H1, embeddings_H1 = generate_embeddings_from_jsonl(json_merged_H1,model_name)
    save_embeddings_to_jsonl(texts_H1,embeddings_H1,output_path)