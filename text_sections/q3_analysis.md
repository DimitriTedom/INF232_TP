# Question 3 - Clustering K-Means des freelances

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

**K retenu : 2** (score de silhouette = 0.366), la
valeur qui maximise le score de silhouette sur la plage testee (K=2 a 8).

## 3. Caracterisation des groupes

- **Cluster 0** (n=118) : TJM moyen = 453.3 EUR, Performance moyenne = 68.1/100
- **Cluster 1** (n=132) : TJM moyen = 310.7 EUR, Performance moyenne = 39.2/100

## 4. Comparaison avec l'etiquette Premium/Standard (a posteriori)

Bien que l'etiquette n'ait pas servi a construire les clusters, il est
interessant de comparer la repartition Premium/Standard au sein de chaque
cluster, pour verifier si le clustering non supervise retrouve une structure
proche de la segmentation commerciale existante :

```
statut   Premium  Standard
cluster                   
0             66        52
1             21       111
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
