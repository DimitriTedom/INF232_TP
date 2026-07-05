"""
BLOC 5 — Régression linéaire simple (TJM → Performance)
Graine : 853155114 (reproductible)
"""

import pathlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "freelances_data.csv"
ASSETS_DIR = BASE_DIR / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

if not DATA_PATH.exists():
    raise FileNotFoundError(f"Données introuvables : {DATA_PATH}. Exécutez src/generate_data.py d'abord.")

df = pd.read_csv(DATA_PATH)

# ---------------------------------------------------------------------------
# CORRÉLATIONS + RÉGRESSION
# ---------------------------------------------------------------------------
corr_pearson = df['tjm_euros'].corr(df['score_performance'], method='pearson')
corr_spearman = df['tjm_euros'].corr(df['score_performance'], method='spearman')

X_r = df[['tjm_euros']]
y_r = df['score_performance']

model = LinearRegression()
model.fit(X_r, y_r)
a = model.coef_[0]
b = model.intercept_
y_pred = model.predict(X_r)
r2 = r2_score(y_r, y_pred)

print("========== Q2 RÉGRESSION ==========")
print(f"Pearson : {corr_pearson:.4f}")
print(f"Spearman : {corr_spearman:.4f}")
print(f"Équation : Performance = {a:.4f} * TJM + {b:.4f}")
print(f"R² : {r2:.4f}")

# ---------------------------------------------------------------------------
# FIGURE (couleur cohérente avec UI)
# ---------------------------------------------------------------------------
sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(9, 6))

sns.scatterplot(data=df, x='tjm_euros', y='score_performance', color='#0F6B62', alpha=0.65, label='Freelances', ax=ax)

tjm_range = np.linspace(df['tjm_euros'].min(), df['tjm_euros'].max(), 100)
tjm_range_df = pd.DataFrame({'tjm_euros': tjm_range})
y_range_pred = model.predict(tjm_range_df)
ax.plot(tjm_range, y_range_pred, color='#C99A3D', linewidth=2.5,
        label=f'Droite de régression (R² = {r2:.3f})')

ax.set_title("Relation entre le Taux Journalier Moyen (TJM) et la Performance", fontweight="bold")
ax.set_xlabel("Taux Journalier Moyen (en €)")
ax.set_ylabel("Score de Performance (sur 100)")
ax.legend(loc='upper left')
fig.tight_layout()

output = ASSETS_DIR / "q2_regression.png"
fig.savefig(output, dpi=300, bbox_inches="tight")
plt.close(fig)
print(f"Graphique sauvegardé : {output}")
