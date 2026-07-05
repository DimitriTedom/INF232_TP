# Rôle : Membre 4 (Analyste Statistique - Question 1)
# Mission : Analyse descriptive univariée de la performance des freelances et détection des outliers (IQR).
# Livrable : Doit exporter 'assets/q1_boxplot.png'.

"""
BLOC 4 — Analyse univariée + détection d'outliers (IQR)
Graine groupe : 853155114 (reproductible)
"""

import pathlib
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "freelances_data.csv"
ASSETS_DIR = BASE_DIR / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)
performance = df["score_performance"]

# ---------------------------------------------------------------------------
# STATISTIQUES DESCRIPTIVES
# ---------------------------------------------------------------------------
print("\n========== STATISTIQUES (Q1) ==========")
print(f"Moyenne      : {performance.mean():.2f}")
print(f"Médiane      : {performance.median():.2f}")
print(f"Variance     : {performance.var(ddof=1):.2f}")
print(f"Ecart-type   : {performance.std(ddof=1):.2f}")

# ---------------------------------------------------------------------------
# OUTLIERS IQR
# ---------------------------------------------------------------------------
Q1 = performance.quantile(0.25)
Q3 = performance.quantile(0.75)
IQR = Q3 - Q1
borne_inf = Q1 - 1.5 * IQR
borne_sup = Q3 + 1.5 * IQR
outliers = df[(performance < borne_inf) | (performance > borne_sup)]

print("\n========== OUTLIERS (IQR) ==========")
print(f"Q1 : {Q1:.2f} | Q3 : {Q3:.2f} | IQR : {IQR:.2f}")
print(f"Borne inf : {borne_inf:.2f} | Borne sup : {borne_sup:.2f}")
print(f"Nombre d'outliers : {len(outliers)}")
if len(outliers) > 0:
    print(outliers[["id_freelance", "tjm_euros", "score_performance", "statut"]])

# ---------------------------------------------------------------------------
# BOITE A MOUSTACHES (sans plt.show pour execution headless)
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(x=performance, ax=ax, color="#0F6B62", width=0.35)
ax.set_title("Boîte à moustaches du score de performance", fontweight="bold")
ax.set_xlabel("Score de performance")
fig.tight_layout()

output_path = ASSETS_DIR / "q1_boxplot.png"
fig.savefig(output_path, dpi=300, bbox_inches="tight")
plt.close(fig)
print(f"\nGraphique sauvegardé : {output_path}")

print("\n========== 10 PREMIERES LIGNES ==========")
print(df.head(10).to_string(index=False))
