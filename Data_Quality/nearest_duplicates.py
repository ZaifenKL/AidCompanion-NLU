


#----Constant Values---------------
embeddings_path = r"C:\AI Stuff\AidCompanion-NLU\Data_Quality"
eps = 0.35
min_samples = 3
#-----Functions--------------------

def detect_near_duplicates(texts, embeddings, eps=0.35, min_samples=2):
    clustering = DBSCAN(eps=eps,min_samples=min_samples,metric="cosine").fit(embeddings)

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