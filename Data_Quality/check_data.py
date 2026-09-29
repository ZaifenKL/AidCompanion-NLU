import os
import json
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_distances

#----Constant Values---------------
embeddings_path = r"C:\AI Stuff\AidCompanion-NLU\Data_Quality"
eps = 0.35
min_samples = 3

#-----Functions--------------------

def load_embeddings_jsonl(path):
    texts = []
    embeddings = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            texts.append(obj["text"])
            embeddings.append(obj["embedding"])

    return texts, np.array(embeddings)


def detect_near_duplicates(texts, embeddings, eps=0.35, min_samples=2):
    clustering = DBSCAN(
        eps=eps,
        min_samples=min_samples,
        metric="cosine"
    ).fit(embeddings)

    labels = clustering.labels_

    clusters = {}
    for idx, cluster_id in enumerate(labels):
        if cluster_id == -1:
            continue
        clusters.setdefault(cluster_id, []).append(texts[idx])

    return clusters


def generate_near_duplicate_report(texts, embeddings, clusters, save_path, lang, hierarchy):

    reports_root = os.path.join(save_path, "Reports", lang, hierarchy)
    os.makedirs(reports_root, exist_ok=True)

    report_path = os.path.join(reports_root, f"{lang}_{hierarchy}_near_duplicates.md")

    with open(report_path, "w", encoding="utf-8") as md:
        md.write(f"# Near-Duplicate Report — {lang}/{hierarchy}\n\n")

        if not clusters:
            md.write("No near-duplicate clusters found.\n")
            return report_path

        for cid, items in clusters.items():

            # --- Extract embeddings for this cluster ---
            idxs = [texts.index(t) for t in items]
            cluster_embs = np.array([embeddings[i] for i in idxs])

            # --- Compute pairwise cosine distances ---
            dist_matrix = cosine_distances(cluster_embs)

            # Flatten distances except diagonal
            flat_distances = dist_matrix[np.triu_indices(len(items), k=1)]

            avg_distance = flat_distances.mean()
            median_distance = np.median(flat_distances)
            min_distance = flat_distances.min()
            max_distance = flat_distances.max()

            # --- Compute cluster centroid ---
            centroid = cluster_embs.mean(axis=0)

            # --- Find most representative text ---
            centroid_distances = cosine_distances(cluster_embs, centroid.reshape(1, -1))
            rep_idx = np.argmin(centroid_distances)
            representative_text = items[rep_idx]

            # --- Write report ---
            md.write(f"## Cluster {cid}\n")
            md.write(f"- Total items: **{len(items)}**\n")
            md.write(f"- Average cosine distance: **{avg_distance:.4f}**\n")
            md.write(f"- Median cosine distance: **{median_distance:.4f}**\n")
            md.write(f"- Minimum cosine distance: **{min_distance:.4f}**\n")
            md.write(f"- Maximum cosine distance: **{max_distance:.4f}**\n")
            md.write(f"- Representative text:\n")
            md.write(f"  > {representative_text}\n\n")

            md.write("### Items in this cluster:\n")
            for t in items:
                md.write(f"- {t}\n")

            md.write("\n---\n\n")

    return report_path


def process_all_embeddings(base_path,eps,min_samples):
    """
    Recibe el path base (ej: Data_Quality)
    Recorre idiomas y jerarquías
    Lee SOLO archivos .jsonl
    Detecta near-duplicates por jerarquía
    Genera reportes Markdown en Data_Quality/Reports/...
    """

    for lang in os.listdir(base_path):
        lang_path = os.path.join(base_path, lang)
        if not os.path.isdir(lang_path):
            continue

        # 🟦 Saltar carpeta Reports/
        if lang == "Reports":
            continue

        for hierarchy in os.listdir(lang_path):
            hierarchy_path = os.path.join(lang_path, hierarchy)
            if not os.path.isdir(hierarchy_path):
                continue

            # 🟦 Buscar SOLO archivos .jsonl dentro de la jerarquía
            jsonl_files = [
                f for f in os.listdir(hierarchy_path)
                if f.lower().endswith(".jsonl")
            ]

            if not jsonl_files:
                print(f"[SKIP] No .jsonl files in {lang}/{hierarchy}")
                continue

            # 🟦 Procesar cada archivo .jsonl encontrado
            for jsonl_file in jsonl_files:
                emb_path = os.path.join(hierarchy_path, jsonl_file)

                print(f"[PROCESSING] {lang}/{hierarchy} → {jsonl_file}")

                texts, embeddings = load_embeddings_jsonl(emb_path)
                clusters = detect_near_duplicates(texts, embeddings,eps,min_samples)

                report = generate_near_duplicate_report(
                    texts,
                    embeddings,
                    clusters,
                    base_path,   # root para Reports/
                    lang,
                    hierarchy
                )

                print(f"[OK] Report saved: {report}")

# -----Sequence-----------
if __name__ == "__main__":

    process_all_embeddings(embeddings_path,eps,min_samples)
