# Justification de l'algorithme de hachage et valeur de la graine (Seed)

Ce document présente la conception, l'implémentation et la justification mathématique de l'algorithme de hachage déterministe développé pour le projet **INF232** (Travail du Membre 1 - Chef de Projet).

---

## 1. Informations du Groupe et Nom Complet Traité

* **Chef de groupe** : TEDOM TAFOTSI DIMITRI WILFRIED
* **Format normalisé (sans accents, sans espaces, en majuscules)** :
  * Conformément à l'exemple illustratif du sujet (`[Prénoms][Nom]`) : **`DIMITRIWILFRIEDTEDOMTAFOTSI`**
  * Format alternatif standard (`[Nom][Prénoms]`) : **`TEDOMTAFOTSIDIMITRIWILFRIED`**

---

## 2. Algorithme de Hachage Choisi : Hachage Polynomial (Rolling Hash)

Pour concevoir une fonction native, robuste et déterministe sans dépendance externe, nous avons implémenté un **hachage polynomial**. Cet algorithme calcule la graine numérique à l'aide de la formule mathématique suivante :

$$H(S) = \left( \sum_{i=0}^{n-1} \text{ord}(S[i]) \cdot p^{n-1-i} \right) \pmod m$$

Où :
* $S$ est la chaîne de caractères normalisée de longueur $n$.
* $\text{ord}(S[i])$ est la valeur ASCII (code numérique) du caractère à l'index $i$.
* $p = 31$ est la base de multiplication (nombre premier).
* $m = 2^{31} - 1$ (2147483647) est le modulo (nombre premier de Mersenne $M_{31}$).

### Justification mathématique et logique de la conception :

1. **Garantie de déterminisme** :
   * L'utilisation de la fonction intégrée `hash()` de Python est à **proscrire** pour ce projet car elle est non-déterministe entre différentes sessions de l'interpréteur (sécurité de randomisation des hashs introduite dans Python 3.3).
   * Notre formule polynomiale dépend uniquement des caractères de la chaîne et de leur ordre, assurant que la graine sera strictement identique à chaque exécution du script.
2. **Sensibilité à l'ordre (Évitement des collisions d'anagrammes)** :
   * Une simple somme des valeurs ASCII des lettres (ex. $\sum \text{ord}(S[i])$) provoquerait de nombreuses collisions entre différents groupes.
   * Le coefficient multiplicatif $p^{n-1-i}$ attribue un poids dépendant de la position de chaque lettre, éliminant ainsi toute collision entre anagrammes.
3. **Choix de la base $p = 31$** :
   * La valeur 31 est un nombre premier impair couramment utilisé (notamment dans l'implémentation de `String.hashCode()` en Java).
   * L'utilisation d'un nombre premier permet de distribuer uniformément les valeurs hachées et de minimiser les collisions lorsque les chaînes possèdent des motifs répétitifs.
4. **Choix du modulo $m = 2^{31} - 1$** :
   * Le nombre $2^{31} - 1$ est le 8ème nombre premier de Mersenne ($M_{31}$).
   * L'application de ce modulo garantit que le résultat final sera un entier positif représentable sur 31 bits ($0 \le H(S) < 2^{31}-1$).
   * Un entier sur 31 bits est universellement compatible avec tous les générateurs de nombres pseudo-aléatoires (PRNG) comme `random.seed()` de Python.

---

## 3. Valeurs de Graine (Seed) Obtenues

Voici les graines numériques calculées selon les formats de nom :

### Option A : Format `[Prénoms][Nom]` (Recommandé - Conforme à l'exemple du TP)
* **Chaîne traitée** : `DIMITRIWILFRIEDTEDOMTAFOTSI`
* **Graine numérique générée** : **`853155114`**

### Option B : Format `[Nom][Prénoms]`
* **Chaîne traitée** : `TEDOMTAFOTSIDIMITRIWILFRIED`
* **Graine numérique générée** : **`354927805`**
