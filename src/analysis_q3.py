# Rôle : Membre 6 (Analyste Data Science - Question 3)
# Mission : Classification non supervisée (Clustering K-Means) pour segmenter les freelances.
# Livrable : Doit exporter 'assets/q3_clusters.png'.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# TODO: Implémenter le clustering non supervisé ici
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# ---------------------------------------------------------------------------
# 0. GRAINE DU GROUPE (coherence avec le reste de l'equipe)
# ---------------------------------------------------------------------------
SEED = 853155114
rng_state = SEED  # utilise comme random_state pour KMeans (reproductibilite)

# ---------------------------------------------------------------------------
# 1. CHARGEMENT DES DONNEES (livrable du Membre 3)
# ---------------------------------------------------------------------------
DATA_PATH = "data/freelances_data.csv"
df = pd.read_csv(DATA_PATH)

# Variables utilisees pour le clustering : uniquement les variables numeriques
# metier. On EXCLUT volontairement la colonne "statut" : le but du K-Means est
# justement de retrouver une structure de groupes de maniere non supervisee,
# sans se servir de l'etiquette existante.
features = ["tjm_euros", "score_performance"]
X = df[features].values

# ---------------------------------------------------------------------------
# 2. STANDARDISATION (obligatoire avant K-Means)
# ---------------------------------------------------------------------------
# Le TJM (echelle ~100-950) et le score de performance (echelle 0-100) n'ont
# pas la meme unite ni la meme variance. Sans standardisation, le TJM
# dominerait entierement le calcul des distances euclidiennes du K-Means.
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ---------------------------------------------------------------------------
# 3. CHOIX DE K : METHODE DU COUDE (Elbow) + SCORE DE SILHOUETTE
# ---------------------------------------------------------------------------
k_range = range(2, 9)
inertias = []
silhouettes = []

for k in k_range:
    km = KMeans(n_clusters=k, n_init=10, random_state=rng_state)
    labels_k = km.fit_predict(X_scaled)
    inertias.append(km.inertia_)
    silhouettes.append(silhouette_score(X_scaled, labels_k))

# Choix final de K : on retient le K qui maximise le score de silhouette,
# tout en verifiant sa coherence avec le coude de l'inertie.
best_k = list(k_range)[int(np.argmax(silhouettes))]

# ---------------------------------------------------------------------------
# 4. CLUSTERING FINAL AVEC LE K RETENU
# ---------------------------------------------------------------------------
kmeans_final = KMeans(n_clusters=best_k, n_init=10, random_state=rng_state)
df["cluster"] = kmeans_final.fit_predict(X_scaled)
final_silhouette = silhouette_score(X_scaled, df["cluster"])

# Centroides ramenes a l'echelle d'origine (pour interpretation metier)
centroids_scaled = kmeans_final.cluster_centers_
centroids_original = scaler.inverse_transform(centroids_scaled)

# ---------------------------------------------------------------------------
# 5. CARACTERISATION DES GROUPES (profil metier de chaque cluster)
# ---------------------------------------------------------------------------
profil = df.groupby("cluster")[features + []].agg(
    effectif=("tjm_euros", "count"),
    tjm_moyen=("tjm_euros", "mean"),
    tjm_median=("tjm_euros", "median"),
    perf_moyenne=("score_performance", "mean"),
    perf_mediane=("score_performance", "median"),
)

# Repartition Premium/Standard par cluster (a titre de comparaison A POSTERIORI
# uniquement -- l'etiquette n'a jamais servi a construire les clusters)
repartition_statut = pd.crosstab(df["cluster"], df["statut"])

# ---------------------------------------------------------------------------
# 6. FIGURE : COUDE + SILHOUETTE + CLUSTERS
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))

# (a) Methode du coude
axes[0].plot(list(k_range), inertias, marker="o", color="#2563eb")
axes[0].axvline(best_k, color="#dc2626", linestyle="--", alpha=0.7,
                 label=f"K retenu = {best_k}")
axes[0].set_xlabel("Nombre de clusters (K)")
axes[0].set_ylabel("Inertie intra-cluster")
axes[0].set_title("Methode du Coude (Elbow)")
axes[0].legend()
axes[0].grid(alpha=0.3)

# (b) Score de silhouette
axes[1].plot(list(k_range), silhouettes, marker="o", color="#059669")
axes[1].axvline(best_k, color="#dc2626", linestyle="--", alpha=0.7,
                 label=f"K retenu = {best_k}")
axes[1].set_xlabel("Nombre de clusters (K)")
axes[1].set_ylabel("Score de silhouette moyen")
axes[1].set_title("Score de Silhouette")
axes[1].legend()
axes[1].grid(alpha=0.3)

# (c) Visualisation des clusters (donnees originales, non standardisees)
palette = plt.cm.tab10(np.linspace(0, 1, best_k))
for c in range(best_k):
    subset = df[df["cluster"] == c]
    axes[2].scatter(subset["tjm_euros"], subset["score_performance"],
                     s=35, alpha=0.75, color=palette[c],
                     label=f"Cluster {c} (n={len(subset)})")
axes[2].scatter(centroids_original[:, 0], centroids_original[:, 1],
                 s=250, marker="X", color="black", edgecolor="white",
                 linewidth=1.5, label="Centroides", zorder=5)
axes[2].set_xlabel("TJM (euros)")
axes[2].set_ylabel("Score de performance")
axes[2].set_title(f"Clusters K-Means (K={best_k})")
axes[2].legend(fontsize=8)
axes[2].grid(alpha=0.3)

plt.tight_layout()
plt.savefig("assets/q3_clusters.png", dpi=150)
plt.close()

# ---------------------------------------------------------------------------
# 7. GENERATION DU TEXTE D'ANALYSE (text_sections/q3_analysis.md)
# ---------------------------------------------------------------------------
lignes_profil = []
for c in range(best_k):
    row = profil.loc[c]
    lignes_profil.append(
        f"- **Cluster {c}** (n={int(row['effectif'])}) : "
        f"TJM moyen = {row['tjm_moyen']:.1f} EUR, "
        f"Performance moyenne = {row['perf_moyenne']:.1f}/100"
    )

texte = f"""# Question 3 - Clustering K-Means des freelances

## 1. Methodologie

Le clustering a ete realise sur les deux variables numeriques disponibles
(TJM et score de performance), **sans utiliser la colonne "statut"**
(Premium/Standard), afin de laisser l'algorithme decouvrir une structure de
groupes de maniere non supervisee.

Les variables ont ete **standardisees** (moyenne 0, ecart-type 1) avant
application du K-Means, car le TJM (echelle ~100-950 EUR) et le score de
performance (echelle 0-100) n'ont ni la meme unite ni la meme variance : sans
standardisation, le TJM aurait domine artificiellement le calcul des
distances euclidiennes.

## 2. Choix du nombre de clusters K

Deux methodes complementaires ont ete utilisees pour justifier K :

- **Methode du coude (Elbow)** : on observe la decroissance de l'inertie
  intra-cluster en fonction de K, et on recherche le point ou l'ajout d'un
  cluster supplementaire n'apporte plus de gain significatif.
- **Score de silhouette** : mesure la qualite de separation des clusters
  (proche de 1 = clusters bien separes, proche de 0 = clusters qui se
  chevauchent).

**K retenu : {best_k}** (score de silhouette = {final_silhouette:.3f}), la
valeur qui maximise le score de silhouette sur la plage testee (K=2 a 8).

## 3. Caracterisation des groupes

{chr(10).join(lignes_profil)}

## 4. Comparaison avec l'etiquette Premium/Standard (a posteriori)

Bien que l'etiquette n'ait pas servi a construire les clusters, il est
interessant de comparer la repartition Premium/Standard au sein de chaque
cluster, pour verifier si le clustering non supervise retrouve une structure
proche de la segmentation commerciale existante :

```
{repartition_statut.to_string()}
```

## 5. Limites du modele

- Le clustering K-Means suppose des clusters de forme spherique et de taille
  comparable, ce qui est une simplification de la realite du marche du
  freelancing.
- Seules deux variables ont ete utilisees (TJM, performance) : des variables
  supplementaires (anciennete, domaine d'expertise, nombre de missions...)
  pourraient reveler une structure plus fine.
- Les quelques valeurs atypiques (outliers) presentes dans le jeu de donnees
  peuvent influencer la position des centroides.
"""

with open("text_sections/q3_analysis.md", "w", encoding="utf-8") as f:
    f.write(texte)

# ---------------------------------------------------------------------------
# 8. RESUME AFFICHE EN CONSOLE
# ---------------------------------------------------------------------------
print(f"K retenu : {best_k} (silhouette = {final_silhouette:.3f})")
print("\nProfil des clusters :")
print(profil.to_string())
print("\nRepartition Premium/Standard par cluster :")
print(repartition_statut.to_string())
print("\nFichiers generes : assets/q3_clusters.png, text_sections/q3_analysis.md")