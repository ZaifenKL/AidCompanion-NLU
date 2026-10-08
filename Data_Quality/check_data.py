import os
import json
from sklearn.cluster import DBSCAN
import numpy as np
from sklearn.metrics.pairwise import cosine_distances
import matplotlib.pyplot as plt

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

# -----------------------------------------
# Histograma de densidad (distancias coseno)
# -----------------------------------------
# -----------------------------------------
# Histograma de densidad (distancias coseno)
# -----------------------------------------
def generate_density_plot(embeddings, out_path, lang, hierarchy):
    dist_matrix = cosine_distances(embeddings)
    flat_distances = dist_matrix[np.triu_indices(len(embeddings), k=1)]

    plt.figure(figsize=(10, 6))
    plt.hist(flat_distances, bins=50, color="steelblue", edgecolor="black")
    plt.title(f"Densidad de Embeddings — {lang}/{hierarchy}")
    plt.xlabel("Distancia coseno")
    plt.ylabel("Frecuencia")
    plt.grid(alpha=0.3)
    plt.savefig(out_path)
    plt.close()

    stats = {
        "min": float(np.min(flat_distances)),
        "max": float(np.max(flat_distances)),
        "mean": float(np.mean(flat_distances)),
        "median": float(np.median(flat_distances)),
        "p10": float(np.percentile(flat_distances, 10)),
        "p90": float(np.percentile(flat_distances, 90)),
    }

    return stats


# -----------------------------------------
# Métodos de detección del codo
# -----------------------------------------

def detect_kneedle(eps_values, cluster_counts):
    """
    Implementación más fiel del algoritmo Kneedle (Satopaa et al., 2011)
    para detectar el codo visual real.
    """

    # Normalizar
    x = (eps_values - np.min(eps_values)) / (np.max(eps_values) - np.min(eps_values))
    y = (cluster_counts - np.min(cluster_counts)) / (np.max(cluster_counts) - np.min(cluster_counts))

    # Línea recta entre inicio y fin
    line = np.linspace(y[0], y[-1], len(y))

    # Diferencia entre curva y línea recta
    diff = y - line

    # El codo es donde la diferencia es máxima
    idx = np.argmax(diff)

    return eps_values[idx]


def detect_max_curvature(eps_values, cluster_counts):
    """
    Detecta el punto donde la curva se dobla más (máxima curvatura).
    Aproximación usando segunda derivada discreta.
    """
    first = np.diff(cluster_counts)
    second = np.diff(first)
    idx = np.argmax(np.abs(second))
    return eps_values[idx+1]


# -----------------------------------------
# Gráfica del codo (eps vs número de clusters)
# -----------------------------------------
def generate_elbow_plot(embeddings, out_path, lang, hierarchy):
    eps_values = np.linspace(0.05, 0.40, 30)
    cluster_counts = []

    for eps in eps_values:
        clustering = DBSCAN(
            eps=eps,
            min_samples=2,
            metric="cosine"
        ).fit(embeddings)

        labels = clustering.labels_
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        cluster_counts.append(n_clusters)

    # Graficar
    plt.figure(figsize=(10, 6))
    plt.plot(eps_values, cluster_counts, marker="o", color="purple")
    plt.title(f"Elbow Plot — {lang}/{hierarchy}")
    plt.xlabel("eps (distancia máxima)")
    plt.ylabel("Número de clusters detectados")
    plt.grid(alpha=0.3)
    plt.savefig(out_path)
    plt.close()

    # --- MÉTODO 1: Codo matemático (mayor caída)
    diffs = np.diff(cluster_counts)
    elbow_math = eps_values[np.argmin(diffs)]

    # --- MÉTODO 2: Kneedle (codo visual)
    elbow_kneedle = detect_kneedle(eps_values, cluster_counts)

    # --- MÉTODO 3: Máxima curvatura
    elbow_curvature = detect_max_curvature(eps_values, cluster_counts)

    return {
        "eps_values": eps_values,
        "cluster_counts": cluster_counts,
        "math": elbow_math,
        "kneedle": elbow_kneedle,
        "curvature": elbow_curvature
    }


# -----------------------------------------
# Reporte Markdown (con rutas relativas)
# -----------------------------------------
def write_markdown_report(md_path, lang, hierarchy, density_png, elbow_png,
                          density_stats, elbow_results):

    density_rel = os.path.basename(density_png)
    elbow_rel = os.path.basename(elbow_png)

    with open(md_path, "w", encoding="utf-8") as md:
        md.write(f"# Reporte de Embeddings — {lang}/{hierarchy}\n\n")

        md.write("## 1. Histograma de densidad\n")
        md.write(f"![Histograma]({density_rel})\n\n")

        md.write("### Estadísticas\n")
        for k, v in density_stats.items():
            md.write(f"- **{k}**: {v:.4f}\n")
        md.write("\n---\n\n")

        md.write("## 2. Gráfica del codo (Elbow)\n")
        md.write(f"![Elbow]({elbow_rel})\n\n")

        md.write("## 3. Comparación de métodos de codo\n\n")
        md.write("| Método | EPS detectado | Interpretación |\n")
        md.write("|--------|---------------|----------------|\n")
        md.write(f"| Matemático | {elbow_results['math']:.3f} | Mayor caída en clusters |\n")
        md.write(f"| Kneedle | {elbow_results['kneedle']:.3f} | Codo visual real |\n")
        md.write(f"| Máxima curvatura | {elbow_results['curvature']:.3f} | Punto donde la curva se dobla más |\n")
        md.write("\n")

        md.write("### Valores probados\n")
        for eps, clusters in zip(elbow_results["eps_values"], elbow_results["cluster_counts"]):
            md.write(f"- eps={eps:.3f} → clusters={clusters}\n")


# -----------------------------------------
# Función principal: recorre todo Data_Quality
# -----------------------------------------
def generate_embedding_report(root_path):
    print(f"[INFO] Buscando embeddings en: {root_path}")

    for lang in os.listdir(root_path):
        lang_path = os.path.join(root_path, lang)
        if not os.path.isdir(lang_path):
            continue

        if lang.lower() == "reports":
            continue

        for hierarchy in os.listdir(lang_path):
            hierarchy_path = os.path.join(lang_path, hierarchy)
            if not os.path.isdir(hierarchy_path):
                continue

            jsonl_files = [
                f for f in os.listdir(hierarchy_path)
                if f.lower().endswith(".jsonl")
            ]

            if not jsonl_files:
                print(f"[SKIP] No .jsonl en {lang}/{hierarchy}")
                continue

            for jsonl_file in jsonl_files:
                jsonl_path = os.path.join(hierarchy_path, jsonl_file)
                print(f"[PROCESSING] {jsonl_path}")

                reports_dir = os.path.join(root_path, "Reports", lang, hierarchy)
                os.makedirs(reports_dir, exist_ok=True)

                density_png = os.path.join(reports_dir, f"{lang}_{hierarchy}_density.png")
                elbow_png = os.path.join(reports_dir, f"{lang}_{hierarchy}_elbow.png")
                md_path = os.path.join(reports_dir, f"{lang}_{hierarchy}_embedding_report.md")

                texts, embeddings = load_embeddings_jsonl(jsonl_path)

                density_stats = generate_density_plot(embeddings, density_png, lang, hierarchy)

                elbow_results = generate_elbow_plot(
                    embeddings, elbow_png, lang, hierarchy
                )

                write_markdown_report(
                    md_path, lang, hierarchy,
                    density_png, elbow_png,
                    density_stats, elbow_results
                )

                print(f"[OK] Reporte generado: {md_path}")

    print("\n[FINISHED] Todos los reportes fueron generados.")

# -----Sequence-----------
if __name__ == "__main__":

    #First we need to undesrtand the distribution of the dataset
    #in this case since its text user input the cosine distances
    generate_embedding_report(embeddings_path)



