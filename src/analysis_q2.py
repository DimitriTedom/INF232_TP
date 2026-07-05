import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# 1. Chargement des données générées par le Membre 3
csv_path = "data/freelances_data.csv"
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"Le fichier de données {csv_path} est introuvable. Veuillez exécuter generate_data.py d'abord.")

df = pd.read_csv(csv_path)

# 2. Analyse de corrélation
# Variable X : tjm_euros
# Variable Y : score_performance
corr_pearson = df['tjm_euros'].corr(df['score_performance'], method='pearson')
corr_spearman = df['tjm_euros'].corr(df['score_performance'], method='spearman')

# 3. Modélisation de la régression linéaire simple
X_r = df[['tjm_euros']]
y_r = df['score_performance']

model = LinearRegression()
model.fit(X_r, y_r)

a = model.coef_[0]
b = model.intercept_
y_pred = model.predict(X_r)
r2 = r2_score(y_r, y_pred)

# Affichage des indicateurs de contrôle pour validation
print(f"Pearson : {corr_pearson:.4f}")
print(f"Spearman : {corr_spearman:.4f}")
print(f"Équation : Performance = {a:.4f} * TJM + {b:.4f}")
print(f"R² : {r2:.4f}")

# 4. Construction de la figure statistique
os.makedirs('assets', exist_ok=True)
plt.figure(figsize=(9, 6))
sns.set_theme(style="whitegrid")

# Nuage de points des freelances
sns.scatterplot(data=df, x='tjm_euros', y='score_performance', color='#2b5c8f', alpha=0.7, label='Freelances')

# Droite de régression linéaire
tjm_range = np.linspace(df['tjm_euros'].min(), df['tjm_euros'].max(), 100).reshape(-1, 1)
tjm_range_df = pd.DataFrame({'tjm_euros': tjm_range.flatten()})
y_range_pred = model.predict(tjm_range_df)
plt.plot(tjm_range.flatten(), y_range_pred, color='#d9534f', linewidth=2.5,
         label=f'Droite de régression (R² = {r2:.3f})')

plt.title("Relation entre le Taux Journalier Moyen (TJM) et la Performance", fontsize=11, fontweight='bold')
plt.xlabel("Taux Journalier Moyen (en €)")
plt.ylabel("Score de Performance (sur 100)")
plt.legend(loc='upper left')
plt.tight_layout()

# Sauvegarde du graphique dans assets
plt.savefig('assets/q2_regression.png', dpi=300)
plt.close()
print("Graphique sauvegardé avec succès dans : assets/q2_regression.png")
