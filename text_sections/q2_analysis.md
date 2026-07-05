# Analyse de la relation entre le TJM et la performance des freelances

**Bloc 5 — Analyste Statistique | Question 2 (Régression)**  
**Thème B — Plateforme de mise en relation freelance / client**  
**Auteur :** KUICHOUO LEOPOLD Stanislas (Membre 5)

---

## 1. Choix méthodologiques et justifications

L'objectif de cette partie est d'étudier la relation entre le niveau de tarification des prestataires, représenté par leur Tarif Journalier Moyen en euros (variable $X$), et leur score de performance historique (variable $Y$).

Pour ce faire, nous procédons en deux étapes :
1. **Analyse de corrélation** : Nous calculons les coefficients de corrélation de **Pearson ($r$)** et de **Spearman ($\rho$)**. Le coefficient de Pearson mesure l'intensité de la relation linéaire globale, tandis que celui de Spearman évalue la relation monotone générale (moins sensible aux valeurs aberrantes et non-linéarités).
2. **Régression linéaire simple** : Nous mettons en œuvre une régression linéaire par la méthode des moindres carrés ordinaires (MCO) pour estimer la performance $\hat{y}$ sous la forme :
   $$\text{Performance} = a \cdot \text{TJM} + b$$
   Ce modèle cherche à déterminer s'il est statistiquement raisonnable d'anticiper la performance d'un nouveau freelance dès son inscription, uniquement sur la base de ses prétentions tarifaires (TJM).

---

## 2. Analyse des résultats numériques

À partir du jeu de données officiel du groupe (généré à partir de la graine **`853155114`**), les calculs statistiques fournissent les résultats suivants :

* **Coefficients de corrélation** :
  * Pearson ($r$) : **`0.2771`** (corrélation positive faible).
  * Spearman ($\rho$) : **`0.3276`** (corrélation monotone faible à modérée).
  * La différence s'explique par la présence de valeurs atypiques injectées dans le jeu de données, qui affaiblissent la relation strictement linéaire.
* **Équation de la droite d'ajustement** :
  $$\text{Performance} = 0.0390 \cdot \text{TJM} + 38.0724$$
  Concrètement, chaque augmentation de **100 €** sur le TJM se traduit par une hausse moyenne estimée de **3.9 points** du score de performance.
* **Qualité de l'ajustement ($R^2$)** :
  * Coefficient de détermination $R^2$ : **`0.0768`** (soit **`7.68%`**).
  * Cela signifie que le TJM n'explique que **7.68%** de la variabilité observée de la performance des freelances. La quasi-totalité de la variance (**92.32%**) est inexpliquée par ce modèle et provient d'autres facteurs non mesurés par le tarif (compétences réelles, expérience, relationnel client).

---

## 3. Synthèse et interprétation pour le commanditaire (Fondatrice)

L'analyse démontre qu'il existe une tendance positive légère : en moyenne, les freelances facturant des tarifs plus élevés ont des scores de performance légèrement meilleurs.

Cependant, sur le plan opérationnel, **il est fortement déconseillé de se baser uniquement sur le TJM d'un nouveau freelance pour prédire sa future performance**. Par exemple, pour un freelance s'inscrivant avec un TJM de 500 €, sa performance théorique estimée par le modèle est de $57.6/100$ ($0.0390 \times 500 + 38.07$), mais en réalité, les observations réelles montrent une dispersion extrême (des freelances à 500 € de TJM ayant des scores réels allant de 15/100 à 90/100). Le TJM n'est pas un signal d'évaluation fiable à lui seul.

---

## 4. Limites du modèle et points de vigilance

L'utilisation de cette régression pour une prédiction automatique présente des faiblesses critiques :
1. **Pouvoir explicatif très faible ($R^2 = 7.68\%$)** : Le modèle ignore $92.3\%$ des causes de la performance. Une décision automatique basée sur ce modèle conduirait à un taux d'erreur inacceptable.
2. **Sensibilité aux valeurs aberrantes** : Le jeu de données contient des profils atypiques voulus (comme des experts facturant peu cher ou des juniors surévalués) qui brisent l'hypothèse de linéarité et tirent la droite de régression vers le bas.
3. **Absence de causalité** : Le TJM reflète le positionnement tarifaire d'un freelance (marketing personnel) et non sa compétence intrinsèque. Augmenter artificiellement le tarif d'un freelance ne rendra pas ses livrables meilleurs.
