# Question 4 — Classification supervisée (Régression Logistique)

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

## 2. Résultats numériques (graine = 853155114)

- **Accuracy** : **73.02%**
- **Recall (classe Premium)** : **68.18%**

Matrice de confusion sur l'ensemble de test (n = 63 ) :

```
                Prédit Standard   Prédit Premium
Réel Standard         31               10
Réel Premium           7               15
```

- Faux positifs (FP = 10) : freelances Standard classés Premium par erreur.
- Faux négatifs (FN = 7) : freelances Premium classés Standard (opportunités manquées).

**Équation logistique (coefficients)** :
```
log-odds(Premium) = -0.8839 + 0.5677 × TJM + 1.2040 × score_performance
```

Les deux coefficients sont de signe positif (TJM) et positif (performance). Le TJM et la performance contribuent tous deux positivement à la probabilité Premium.

## 3. Synthèse à destination de la fondatrice (risques business)

Avec une accuracy de 73%, le modèle fait mieux qu'un classifieur naïf qui prédirait toujours « Standard » (majoritaire ~65 %). Cependant, la performance reste modérée car la corrélation entre TJM/performance et le statut « au feeling » de l'équipe commerciale n'est pas très forte (cf. Question 2).

**Risques concrets identifiés :**

- **Faux positifs (dilution de la marque Premium)** : 10 profils sur l'échantillon de test ont été sur-valorisés. Si on les oriente vers des clients exigeants ou des missions haut de gamme sans vérification supplémentaire, on risque une déception client et une atteinte à la réputation de la catégorie « Premium ».

- **Faux négatifs (opportunités ratées)** : 7 bons profils ont été sous-classés. Ces freelances risquent d'être sous-exploités (moins de visibilité, missions moins rémunératrices), ce qui peut les pousser à quitter la plateforme pour la concurrence.

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
