# Rôle : Membre 4 (Analyste Statistique - Question 1)
# Mission : Analyse descriptive univariée de la performance des freelances et détection des outliers (IQR).
# Livrable : Doit exporter 'assets/q1_boxplot.png'.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# TODO: Implémenter l'analyse univariée ici
# Rôle : Membre 4 (Analyste Statistique - Question 1)
# Mission : Analyse descriptive univariée de la performance des freelances et détection des outliers (IQR).

import pathlib

# Chargement des données
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "freelances_data.csv"
df = pd.read_csv(DATA_PATH)

# ---------------------------------------------------------------------------
# 8. ANALYSE STATISTIQUE
# ---------------------------------------------------------------------------

performance = df["score_performance"]

print("\n========== STATISTIQUES ==========")
print(f"Moyenne      : {performance.mean():.2f}")
print(f"Médiane      : {performance.median():.2f}")
print(f"Variance     : {performance.var(ddof=1):.2f}")
print(f"Ecart-type   : {performance.std(ddof=1):.2f}")

# ---------------------------------------------------------------------------
# 9. DETECTION DES OUTLIERS (IQR)
# ---------------------------------------------------------------------------

Q1 = performance.quantile(0.25)
Q3 = performance.quantile(0.75)
IQR = Q3 - Q1

borne_inf = Q1 - 1.5 * IQR
borne_sup = Q3 + 1.5 * IQR

outiers = df[(performance < borne_inf) | (performance > borne_sup)]

print("\n========== OUTLIERS ==========")
print(f"Q1 : {Q1:.2f}")
print(f"Q3 : {Q3:.2f}")
print(f"IQR : {IQR:.2f}")
print(f"Borne inférieure : {borne_inf:.2f}")
print(f"Borne supérieure : {borne_sup:.2f}")
print(f"Nombre d'outliers : {len(outiers)}")

if len(outiers) > 0:
    print(outiers)

# ---------------------------------------------------------------------------
# 10. BOITE A MOUSTACHES
# ---------------------------------------------------------------------------

plt.figure(figsize=(8,5))
sns.boxplot(x=performance)
plt.title("Boîte à moustaches du score de performance")
plt.xlabel("Score de performance")
plt.tight_layout()

output_path = BASE_DIR / "assets" / "q1_boxplot.png"
output_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(output_path, dpi=300)
plt.show()

# ---------------------------------------------------------------------------
# 11. 10 PREMIERES LIGNES
# ---------------------------------------------------------------------------

print("\n========== 10 PREMIERES LIGNES ==========")
print(df.head(10).to_string(index=False))
