# INF232 — Projet d'Analyse de Données & Statistique (Groupe 01)
## Thème B : Plateforme de mise en relation freelance/client

Ce dépôt contient le projet d'analyse statistique et de classification pour le cours **INF232**. Il est structuré pour permettre une collaboration fluide entre les 10 membres du groupe.

---

## 🚀 Mode d'emploi (Exécution rapide)

```bash
pip install numpy pandas matplotlib seaborn scikit-learn streamlit
python src/generate_data.py          # (si data/ absent)
python src/analysis_q1.py            # optionnel : régénère assets
python src/analysis_q2.py
python src/analysis_q3.py
python src/analysis_q4.py            # Bloc 7 complété
streamlit run src/app.py
```

L'app affiche les PNG officiels si présents dans `assets/`, sinon génère les graphiques automatiquement (même logique que les scripts analysis).

---

## 👥 Coordination du Groupe & Répartition des Tâches (10 Blocs)

Le projet est divisé en 10 rôles spécifiques pour assurer la livraison du TP dans les délais.

### 📦 BLOC 1 : Chef de Projet — Graine & Coordination (Fait ✅)
* **Membre responsable** : Membre 1 (Chef de groupe : Dimitri Tedom)
* **Outils** : Python (Fonction native).
* **Mission** : Normalisation du nom du chef de groupe, conception et implémentation du hachage polynomial déterministe pour générer la graine numérique du groupe.
* **Livrables produits** :
  * [src/graine.py](file:///C:/Users/Dimitri%20SnowDev/Documents/TP%20232/INF232_TP_GROUPE01/src/graine.py) (script contenant uniquement la fonction de hachage).
  * [text_sections/justification_graine.md](file:///C:/Users/Dimitri%20SnowDev/Documents/TP%20232/INF232_TP_GROUPE01/text_sections/justification_graine.md) (justification mathématique et logique de l'algorithme).
* **Graine obtenue** : `853155114` (à utiliser par le Membre 3 pour la génération).

### 🗃️ BLOC 2 : Architecte de Données — Modélisation du Jeu de Données (Fait ✅)
* **Membre responsable** : Membre 2 (MAMBOUNE NCHOURUPOUO BASMA)
* **Outils** : Spécifications théoriques (Texte/Markdown).
* **Mission** : Définir la plausibilité et la structure des variables du dataset pour le Thème B :
  * **Variable 1** : Score de performance (de 0 à 100).
  * **Variable 2** : TJM (Tarif Journalier Moyen de 100€ à 950€).
  * **Étiquette** : Classification commerciale subjective (Premium / Standard).
  * Justifier la taille de l'échantillon ($N = 250$ freelances) pour les tests.
* **Livrables produits** : [text_sections/m2_justification.md](file:///C:/Users/Dimitri%20SnowDev/Documents/TP%20232/INF232_TP_GROUPE01/text_sections/m2_justification.md) (spécification des plages de valeurs et justification rédigée).
* **À envoyer à** : Membre 3 (pour coder le générateur) et Membre 10 (pour intégration au rapport).

### 💻 BLOC 3 : Développeur Data — Pipeline de Génération & Export (Fait ✅)
* **Membre responsable** : Membre 3 (MELI TANGA JEEPS PARVEL)
* **Outils** : Python, bibliothèque `numpy` (fixer `np.random.seed(853155114)`).
* **Mission** : Coder le script de génération de données déterministe à partir de la structure définie par le Membre 2 et de la graine du Membre 1.
* **Livrables produits** : [src/generate_data.py](file:///C:/Users/Dimitri%20SnowDev/Documents/TP%20232/INF232_TP_GROUPE01/src/generate_data.py) (script de génération) et [data/freelances_data.csv](file:///C:/Users/Dimitri%20SnowDev/Documents/TP%20232/INF232_TP_GROUPE01/data/freelances_data.csv) (jeu de données généré).
* **À envoyer à** : Membres 4, 5, 6, 7 (qui ont besoin du CSV), Membre 9 (pour l'application) et Membre 10 (pour le rapport).

### 📊 BLOC 4 : Analyste Statistique — Question 1 (Statistique Univariée)
* **Membre responsable** : Membre 4 (NGONO DANIELLE STEPHANIE ESTELLE)
* **Outils** : Python (`pandas`, `matplotlib`, `seaborn`).
* **Mission** : Analyser la distribution de la performance des freelances. Calculer la moyenne, médiane, variance, écart-type. Détecter les valeurs aberrantes (outliers) par la méthode IQR de Tukey. Rédiger la vulgarisation pour les investisseurs et les limites des données.
* **Livrable** : Code de calcul, graphique boîte à moustaches (`assets/q1_boxplot.png`), et rapport textuel rédigé.
* **À envoyer à** : Membre 8 (UI), Membre 9 (App) et Membre 10 (Rapport).

### 📈 BLOC 5 : Analyste Statistique — Question 2 (Régression Bivariée) (Fait ✅)
* **Membre responsable** : Membre 5 (KUICHOUO LEOPOLD Stanislas)
* **Outils** : Python (`scipy.stats` ou `scikit-learn`, `seaborn`).
* **Mission** : Modéliser la relation entre la performance et le TJM. Calculer les corrélations de Pearson et Spearman. Calculer l'équation de la droite de régression linéaire simple ($y = ax + b$). Calculer le $R^2$ et évaluer la viabilité et les limites de la prédiction de performance à partir du TJM.
* **Livrables produits** : [src/analysis_q2.py](file:///C:/Users/Dimitri%20SnowDev/Documents/TP%20232/INF232_TP_GROUPE01/src/analysis_q2.py) (code de régression), [assets/q2_regression.png](file:///C:/Users/Dimitri%20SnowDev/Documents/TP%20232/INF232_TP_GROUPE01/assets/q2_regression.png) (graphique de régression) et [text_sections/q2_analysis.md](file:///C:/Users/Dimitri%20SnowDev/Documents/TP%20232/INF232_TP_GROUPE01/text_sections/q2_analysis.md) (rapport d'analyse rédigé).
* **À envoyer à** : Membre 8 (UI), Membre 9 (App) et Membre 10 (Rapport).

### 🔍 BLOC 6 : Analyste Data Science — Question 3 (Clustering non supervisé) (Fait ✅)
* **Membre responsable** : Membre 6 (LAMBO LEKOUBOU DIMITRI)
* **Outils** : Python (`scikit-learn` pour KMeans, `matplotlib`).
* **Mission** : Segmenter les freelances sans utiliser le label historique. Standardiser les données au préalable. Justifier le nombre optimal de groupes (Elbow + Silhouette). Dresser le profil commercial de chaque groupe.
* **Livrables produits** : `src/analysis_q3.py`, `assets/q3_clusters.png`, `text_sections/q3_analysis.md`.
* **À envoyer à** : Membre 8 (UI), Membre 9 (App) et Membre 10 (Rapport).

### 🤖 BLOC 7 : Analyste Data Science — Question 4 (Classification supervisée) (Fait ✅)
* **Membre responsable** : Membre 7 (TEKENG KAMWÉLÉ JUNIOR CAMBELL)
* **Outils** : Python (`scikit-learn` : LogisticRegression + StandardScaler + train_test_split).
* **Mission** : Entraîner un classifieur pour prédire Premium/Standard. Matrice de confusion, accuracy, recall (Premium). Évaluer risques business (FP = dilution marque ; FN = opportunités ratées).
* **Livrables produits** : `src/analysis_q4.py`, `assets/q4_matrix.png`, `text_sections/q4_analysis.md`.
* **À envoyer à** : Membre 8 (UI), Membre 9 (App) et Membre 10 (Rapport).

### 🎨 BLOC 8 : Développeur Front / UI — Visualisation & Interface Web (Fait ✅)
* **Membre responsable** : Membre 8 (Nguefah zeutcha Carol junior)
* **Outils** : Python + Streamlit (design tokens, onglets par question, fallback génération auto).
* **Mission** : Maquette UI complète en onglets + design pro (couleurs par section, cartes métriques, reproductibilité visible).
* **Livrable** : UI intégrée dans `src/app.py` (maquette fournie + packaging).

### 🛠️ BLOC 9 : Intégrateur Dev — Packaging Application & Exécution (Fait ✅)
* **Membre responsable** : Membre 9 (NKONZAP ARIANE)
* **Outils** : Python, Streamlit, Git.
* **Mission** : Fusionner l'interface du Membre 8 avec les codes de calcul et de visualisation des Membres 3, 4, 5, 6, 7 dans `src/app.py`. Rédiger un README d'exécution et tester le bon fonctionnement local.
* **Livrable** : `src/app.py` fonctionnel avec tous les onglets et graphiques.

### ✍️ BLOC 10 : Éditeur en Chef — Assemblage & Compilation du Rapport
* **Membre responsable** : Membre 10 (YONKOUA YANN LUCA)
* **Outils** : LaTeX, Google Docs ou Word, PDF.
* **Mission** : Collecter les parties textuelles rédigées, les équations et les graphiques de tous les membres. Rédiger l'introduction générale, inclure la justification obligatoire de l'usage de Python. Compiler en Rapport.pdf, structurer le dossier final du groupe et effectuer le dépôt avant 23h59.
* **Livrable** : Rapport.pdf à la racine et dépôt du ZIP final.

---

## 📂 Organisation de l'arbre de fichiers du dépôt

```text
INF232_TP_GROUPE01/
├── data/
│   └── freelances_data.csv       <-- Généré par le Membre 3 (Fait ✅)
├── src/
│   ├── graine.py                 <-- Code du Membre 1 (Fait ✅)
│   ├── generate_data.py          <-- Code du Membre 3 (Fait ✅)
│   ├── analysis_q1.py            <-- Code du Membre 4 (Fait ✅)
│   ├── analysis_q2.py            <-- Code du Membre 5 (Fait ✅)
│   ├── analysis_q3.py            <-- Code du Membre 6 (Fait ✅)
│   ├── analysis_q4.py            <-- Code du Membre 7 (Fait ✅)
│   └── app.py                    <-- Interface Streamlit intégrée (M8/M9 - Fait ✅)
├── assets/
│   ├── q1_boxplot.png            <-- Graphique du Membre 4 (Fait ✅)
│   ├── q2_regression.png         <-- Graphique du Membre 5 (Fait ✅)
│   ├── q3_clusters.png           <-- Graphique du Membre 6 (Fait ✅)
│   └── q4_matrix.png             <-- Graphique du Membre 7 (Fait ✅)
├── text_sections/
│   ├── justification_graine.md   <-- Justification de la graine du Membre 1 (Fait ✅)
│   ├── m2_justification.md       <-- Justification de la modélisation du Membre 2 (Fait ✅)
│   ├── q1_analysis.md            <-- Analyse Membre 4 (Fait ✅)
│   ├── q2_analysis.md            <-- Analyse Membre 5 (Fait ✅)
│   ├── q3_analysis.md            <-- Analyse Membre 6 (Fait ✅)
│   └── q4_analysis.md            <-- Analyse Membre 7 (Fait ✅)
├── README.md                     <-- Ce fichier de coordination et notice (Fait ✅)
└── Rapport.pdf                   <-- Rapport PDF final assemblé par le Membre 10 (à venir)
```
