"""
INF232 - TP Statistiques et Analyse de Données
Theme B : Plateforme freelance/client
BLOC 3 : Pipeline de generation des donnees (Membre 3)

Ce script genere de maniere DETERMINISTE le jeu de donnees des freelances,
a partir :
  - de la graine du groupe fournie par le Membre 1 : 853155114
    (obtenue via l'algorithme nom -> graine documente dans le rapport)
  - de la structure des variables definie et justifiee par le Membre 2 :
      * TJM (Tarif Journalier Moyen)   : quantitative continue, bornes [100, 950]
      * Score de Performance            : quantitative discrete,  bornes [0, 100]
      * Statut (etiquette)              : qualitative nominale, Premium / Standard
      * Taille de l'echantillon         : N = 250 (justifie par le Membre 2, TCL)

Choix de conception statistique assumes par le Membre 3 (a documenter dans le
rapport, section generation des donnees) :

1. CORRELATION TJM / PERFORMANCE
   Le sujet (Question 2 du theme B) suppose une relation entre le TJM et la
   performance. Pour eviter une correlation parfaite (peu realiste) ou une
   independance totale (qui rendrait la Question 2 vide de sens), on introduit
   un facteur latent "qualite globale" du freelance qui influence les deux
   variables, chacune recevant en plus un bruit independant.

2. ETIQUETTE PROBABILISTE (et non un seuil brut)
   Le Membre 2 precise que le statut Premium est attribue par l'equipe
   commerciale "en fonction" du TJM et de la performance, mais que ce
   classement a ete fait "un peu au feeling" (cf. Question 3 du theme). On
   modelise donc l'etiquette comme une fonction LOGISTIQUE (probabiliste) des
   deux variables normalisees, et non comme une regle deterministe stricte.
   Cela garantit que la classification supervisee (Question 4) est possible
   mais imparfaite, ce qui est plus realiste et permet une vraie discussion
   des limites du modele.

3. VALEURS ATYPIQUES (outliers)
   Pour que la Question 1 (statistique univariee) ait des cas concrets de
   valeurs "hors norme" a detecter, quelques individus (toujours tires du
   generateur a graine fixe, donc reproductibles) recoivent des valeurs
   extremes de TJM et/ou de performance.

Determinisme : relancer ce script avec la meme graine reproduit exactement le
meme fichier CSV, caractere pour caractere.
"""

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# 0. GRAINE DU GROUPE (fournie par le Membre 1)
# ---------------------------------------------------------------------------
SEED = 853155114
rng = np.random.default_rng(SEED)

# ---------------------------------------------------------------------------
# 1. PARAMETRES DE STRUCTURE (fournis/justifies par le Membre 2)
# ---------------------------------------------------------------------------
N = 250                # taille de l'echantillon (justifiee : N >> 30, TCL)
TJM_MIN, TJM_MAX = 100, 950
PERF_MIN, PERF_MAX = 0, 100
N_OUTLIERS = 8          # ~3% de l'echantillon, valeurs extremes controlees

# ---------------------------------------------------------------------------
# 2. FACTEUR LATENT DE "QUALITE GLOBALE" (mecanisme de correlation)
# ---------------------------------------------------------------------------
# Loi normale centree reduite : sert de facteur commun aux deux variables.
qualite = rng.normal(loc=0.0, scale=1.0, size=N)

# ---------------------------------------------------------------------------
# 3. GENERATION DU TJM (Tarif Journalier Moyen)
# ---------------------------------------------------------------------------
# Base realiste : distribution asymetrique a droite (peu de tres hauts TJM),
# obtenue via une loi gamma, a laquelle on ajoute l'effet du facteur qualite
# et un bruit propre.
tjm_base = rng.gamma(shape=2.2, scale=140, size=N)     # asymetrie realiste
tjm_bruit = rng.normal(0, 60, size=N)                   # bruit propre au TJM
tjm_brut = tjm_base + 90 * qualite + tjm_bruit

# Normalisation (min-max) puis mise a l'echelle dans les bornes [100, 950]
tjm_scaled = (tjm_brut - tjm_brut.min()) / (tjm_brut.max() - tjm_brut.min())
tjm = TJM_MIN + tjm_scaled * (TJM_MAX - TJM_MIN)

# ---------------------------------------------------------------------------
# 4. GENERATION DU SCORE DE PERFORMANCE
# ---------------------------------------------------------------------------
perf_bruit = rng.normal(0, 12, size=N)                  # bruit propre a la perf.
perf_brut = 55 + 14 * qualite + perf_bruit              # centre ~55/100

# Clip dans les bornes puis arrondi (variable quantitative discrete)
performance = np.clip(perf_brut, PERF_MIN, PERF_MAX)
performance = np.round(performance).astype(int)

# ---------------------------------------------------------------------------
# 5. INJECTION D'OUTLIERS CONTROLES (toujours via le RNG a graine fixe)
# ---------------------------------------------------------------------------
outlier_idx = rng.choice(N, size=N_OUTLIERS, replace=False)
for i in outlier_idx:
    if rng.random() < 0.5:
        # outlier "TJM extreme" (tres bas ou tres haut)
        tjm[i] = TJM_MIN if rng.random() < 0.5 else TJM_MAX - rng.uniform(0, 10)
    else:
        # outlier "performance extreme"
        performance[i] = PERF_MIN if rng.random() < 0.5 else PERF_MAX

tjm = np.round(tjm, 1)

# ---------------------------------------------------------------------------
# 6. GENERATION DE L'ETIQUETTE (Premium / Standard) - fonction logistique
# ---------------------------------------------------------------------------
tjm_norm = (tjm - tjm.min()) / (tjm.max() - tjm.min())
perf_norm = (performance - performance.min()) / (performance.max() - performance.min())

# Score composite : moyenne ponderee des deux variables normalisees
score_composite = 0.55 * tjm_norm + 0.45 * perf_norm

# Fonction logistique : probabilite d'etre Premium en fonction du score composite.
# Seuil place au 70e percentile (et non la moyenne) car, d'apres la justification
# metier du Membre 2, "Premium" est une DISTINCTION reservee aux meilleurs
# profils : elle doit rester minoritaire (~25-30% de l'echantillon), pas un
# partage 50/50. Le facteur 8 controle la "nettete" de la separation (ni
# parfaite -> classification supervisee triviale, ni trop floue -> injustifiable).
seuil = np.quantile(score_composite, 0.78)
proba_premium = 1 / (1 + np.exp(-10 * (score_composite - seuil)))

tirage = rng.random(N)
statut = np.where(tirage < proba_premium, "Premium", "Standard")

# ---------------------------------------------------------------------------
# 7. ASSEMBLAGE ET EXPORT
# ---------------------------------------------------------------------------
df = pd.DataFrame({
    "id_freelance": np.arange(1, N + 1),
    "tjm_euros": tjm,
    "score_performance": performance,
    "statut": statut,
})

output_path = "data/freelances_data.csv"
df.to_csv(output_path, index=False, encoding="utf-8")

print(f"Graine utilisee : {SEED}")
print(f"Nombre de lignes generees : {len(df)}")
print(f"Repartition des statuts :\n{df['statut'].value_counts()}\n")
print("10 premieres lignes :")
print(df.head(10).to_string(index=False))
