# Rôle : Membre 7 (Analyste Data Science - Question 4)
# Mission : Classification supervisée (Régression logistique) pour classifier les profils (Premium / Standard).
# Livrable : Doit exporter 'assets/q4_matrix.png' et text_sections/q4_analysis.md .

"""
BLOC 7 — Classification supervisée (Régression Logistique)
Thème B : Plateforme Freelance/Client

Objectif (Question 4) :
Prédire automatiquement le statut "Premium" ou "Standard" d'un nouveau freelance
à partir de ses deux indicateurs mesurables (TJM et score de performance),
pour automatiser l'orientation commerciale dès l'inscription.

Approche :
- Régression logistique (modèle linéaire interprétable, probabiliste)
- Standardisation des features (cohérent avec le clustering du Membre 6)
- Split stratifié 75/25 pour préserver la proportion des classes
- Métriques : Accuracy globale + Recall sur la classe Premium (priorité business : ne pas rater les bons profils)
- Visualisation : Matrice de confusion (heatmap)

Graine du groupe utilisée pour reproductibilité : 853155114
"""

import pathlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, recall_score, confusion_matrix

# ---------------------------------------------------------------------------
# 0. CONFIG & GRAINE (cohérence avec l'ensemble du projet)
# ---------------------------------------------------------------------------
SEED = 853155114
sns.set_theme(style="whitegrid")

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "freelances_data.csv"
ASSETS_DIR = BASE_DIR / "assets"
TEXT_DIR = BASE_DIR / "text_sections"

ASSETS_DIR.mkdir(parents=True, exist_ok=True)
TEXT_DIR.mkdir(parents=True, exist_ok=True)

# Couleur "brique" pour Q4 (cohérente avec la maquette UI du Membre 8)
ACCENT_Q4 = "#B4463A"

# ---------------------------------------------------------------------------
# 1. CHARGEMENT DES DONNÉES (livrable Membre 3)
# ---------------------------------------------------------------------------
df = pd.read_csv(DATA_PATH)
print(f"Données chargées : {len(df)} freelances")
print(f"Répartition statut : \n{df['statut'].value_counts()}\n")

# ---------------------------------------------------------------------------
# 2. PRÉPARATION : Features + Target
# ---------------------------------------------------------------------------
features = ["tjm_euros", "score_performance"]
X = df[features]
y = (df["statut"] == "Premium").astype(int)  # 1 = Premium, 0 = Standard

# ---------------------------------------------------------------------------
# 3. TRAIN / TEST SPLIT (stratifié + reproductible)
# ---------------------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=SEED, stratify=y
)
print(f"Split : train={len(X_train)}, test={len(X_test)} (stratifié)")

# ---------------------------------------------------------------------------
# 4. STANDARDISATION (obligatoire pour régression logistique avec régularisation implicite)
# ---------------------------------------------------------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ---------------------------------------------------------------------------
# 5. ENTRAÎNEMENT DU MODÈLE
# ---------------------------------------------------------------------------
modele = LogisticRegression(random_state=SEED, max_iter=1000)
modele.fit(X_train_scaled, y_train)

y_pred = modele.predict(X_test_scaled)

# ---------------------------------------------------------------------------
# 6. MÉTRIQUES D'ÉVALUATION
# ---------------------------------------------------------------------------
accuracy = accuracy_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)  # recall sur Premium (classe positive)
matrice = confusion_matrix(y_test, y_pred)

tn, fp, fn, tp = matrice.ravel()

print("\n========== MÉTRIQUES ==========")
print(f"Accuracy  : {accuracy:.4f} ({accuracy:.2%})")
print(f"Recall (Premium) : {recall:.4f} ({recall:.2%})")
print(f"Matrice de confusion (lignes = réel, colonnes = prédit) :")
print(f"          Standard  Premium")
print(f"Standard     {tn:3d}      {fp:3d}")
print(f"Premium      {fn:3d}      {tp:3d}")
print(f"\nFP (faux Premium) = {fp} | FN (manqués Premium) = {fn}")

# Coefs pour interprétation
coef_tjm = modele.coef_[0][0]
coef_perf = modele.coef_[0][1]
intercept = modele.intercept_[0]
print(f"\nCoefficients du modèle :")
print(f"  log-odds(Premium) = {intercept:.4f} + {coef_tjm:.4f}*TJM + {coef_perf:.4f}*Perf")

# ---------------------------------------------------------------------------
# 7. VISUALISATION : MATRICE DE CONFUSION
# ---------------------------------------------------------------------------
cmap_q4 = sns.light_palette(ACCENT_Q4, as_cmap=True)

fig, ax = plt.subplots(figsize=(6.8, 5.8))
sns.heatmap(
    matrice,
    annot=True,
    fmt="d",
    cmap=cmap_q4,
    cbar=False,
    xticklabels=["Standard", "Premium"],
    yticklabels=["Standard", "Premium"],
    annot_kws={"size": 16, "weight": "bold"},
    linewidths=1.5,
    linecolor="white",
    ax=ax,
)
ax.set_title(
    f"Matrice de confusion — Régression Logistique\n"
    f"Accuracy = {accuracy:.2%}  |  Recall (Premium) = {recall:.2%}",
    fontweight="bold",
    pad=12,
)
ax.set_xlabel("Statut prédit", fontsize=11)
ax.set_ylabel("Statut réel", fontsize=11)
fig.tight_layout()

output_png = ASSETS_DIR / "q4_matrix.png"
plt.savefig(output_png, dpi=300, bbox_inches="tight")
plt.close()
print(f"\nGraphique sauvegardé : {output_png}")

# ---------------------------------------------------------------------------
# 8. GÉNÉRATION DU RAPPORT TEXTUEL (text_sections/q4_analysis.md)
# ---------------------------------------------------------------------------
# Interprétation métier des coefs
direction_tjm = "positif" if coef_tjm > 0 else "négatif"
direction_perf = "positif" if coef_perf > 0 else "négatif"
impact = "Le TJM et la performance contribuent tous deux positivement à la probabilité Premium." if coef_tjm > 0 and coef_perf > 0 else "Interprétation à nuancer selon les signes."

texte_analyse = f"""# Question 4 — Classification supervisée (Régression Logistique)

**BLOC 7 — Analyste Data Science | Membre 7**  
**Thème B : Plateforme de mise en relation freelance / client**

## 1. Objectif et justification de la méthode

La fondatrice souhaite automatiser l'orientation commerciale : à l'inscription d'un nouveau freelance, prédire s'il doit être traité comme « Premium » ou « Standard » **uniquement à partir du TJM déclaré et du score de performance historique**.

Nous utilisons la **régression logistique** pour les raisons suivantes :
- Modèle probabiliste interprétable (on obtient des probas + coefficients lisibles).
- Rapide à entraîner et à expliquer à une équipe non technique.
- Cohérent avec les variables déjà utilisées dans les Questions 2 et 3.
- Permet une discussion fine des risques business (faux positifs vs faux négatifs).

**Pré-traitement important** (cohérence avec le Membre 6) :
- Standardisation des deux variables (moyenne 0, écart-type 1) avant l'entraînement.
- Split train/test 75 % / 25 % **stratifié** pour préserver la proportion des classes (environ 35 % Premium dans le jeu global).

## 2. Résultats numériques (graine = {SEED})

- **Accuracy** : **{accuracy:.2%}**
- **Recall (classe Premium)** : **{recall:.2%}**

Matrice de confusion sur l'ensemble de test (n = {len(X_test)} ) :

```
                Prédit Standard   Prédit Premium
Réel Standard        {tn:3d}              {fp:3d}
Réel Premium         {fn:3d}              {tp:3d}
```

- Faux positifs (FP = {fp}) : freelances Standard classés Premium par erreur.
- Faux négatifs (FN = {fn}) : freelances Premium classés Standard (opportunités manquées).

**Équation logistique (coefficients)** :
```
log-odds(Premium) = {intercept:.4f} + {coef_tjm:.4f} × TJM + {coef_perf:.4f} × score_performance
```

Les deux coefficients sont de signe {direction_tjm} (TJM) et {direction_perf} (performance). {impact}

## 3. Synthèse à destination de la fondatrice (risques business)

Avec une accuracy de {accuracy:.0%}, le modèle fait mieux qu'un classifieur naïf qui prédirait toujours « Standard » (majoritaire ~65 %). Cependant, la performance reste modérée car la corrélation entre TJM/performance et le statut « au feeling » de l'équipe commerciale n'est pas très forte (cf. Question 2).

**Risques concrets identifiés :**

- **Faux positifs (dilution de la marque Premium)** : {fp} profils sur l'échantillon de test ont été sur-valorisés. Si on les oriente vers des clients exigeants ou des missions haut de gamme sans vérification supplémentaire, on risque une déception client et une atteinte à la réputation de la catégorie « Premium ».

- **Faux négatifs (opportunités ratées)** : {fn} bons profils ont été sous-classés. Ces freelances risquent d'être sous-exploités (moins de visibilité, missions moins rémunératrices), ce qui peut les pousser à quitter la plateforme pour la concurrence.

**Recommandation opérationnelle** :
Ne pas utiliser le modèle seul pour une décision définitive. L'utiliser comme **score d'aide à la décision** : 
- Si probabilité prédite > 0.65 → proposition Premium + revue rapide par l'équipe commerciale.
- Si probabilité < 0.35 → Standard par défaut.
- Zone grise (0.35-0.65) → examen humain obligatoire.

## 4. Analyse critique et limites

- Le statut « Premium/Standard » a été attribué « un peu au feeling » (cf. énoncé). Le modèle apprend donc les biais et intuitions passées de l'équipe commerciale plutôt qu'une vérité objective.
- Seules deux variables sont disponibles. L'ajout de features métier (domaine d'expertise, ancienneté, taux de complétion des missions, notes clients...) améliorerait fortement la discrimination.
- La régression logistique suppose une relation linéaire dans l'espace logit. Des modèles non linéaires (Random Forest, Gradient Boosting) pourraient capturer des interactions plus fines, au prix d'une moindre interprétabilité.
- L'échantillon est synthétique et déterministe. Les performances observées sont indicatives ; un test sur de vraies données opérationnelles est indispensable avant déploiement.

Le modèle est **raisonnable comme premier outil d'aide**, mais **insuffisant pour une automatisation aveugle** sans supervision humaine sur les cas limites.
"""

md_path = TEXT_DIR / "q4_analysis.md"
with open(md_path, "w", encoding="utf-8") as f:
    f.write(texte_analyse)

print(f"\nAnalyse textuelle générée : {md_path}")
print("\n========== BLOC 7 TERMINÉ ==========")
print("Fichiers produits : assets/q4_matrix.png + text_sections/q4_analysis.md")

