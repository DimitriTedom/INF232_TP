# INF232 — Projet d'Analyse de Données & Statistique (Groupe 14)
## Thème B : Plateforme de mise en relation freelance/client

Ce dépôt contient le projet d'analyse statistique et de classification pour le cours **INF232**. Il est structuré pour permettre une collaboration fluide entre les 10 membres du groupe.

---

## 🚀 Mode d'emploi (Exécution rapide)

Pour installer les dépendances et exécuter l'application interactive Streamlit, lancez les commandes suivantes dans votre terminal :
```bash
pip install numpy pandas matplotlib seaborn scikit-learn streamlit
python src/generate_data.py
streamlit run src/app.py
```

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

### 🔍 BLOC 6 : Analyste Data Science — Question 3 (Clustering non supervisé)
* **Membre responsable** : Membre 6
* **Outils** : Python (`scikit-learn` pour KMeans ou CAH, `matplotlib`).
* **Mission** : Segmenter les freelances sans utiliser le label historique. Standardiser les données au préalable. Justifier le nombre optimal de groupes (Elbow method et/ou Silhouette score). Dresser le profil commercial de chaque groupe découvert et discuter des limites de l'algorithme.
* **Livrable** : Code de clustering, graphiques de sélection et de visualisation des classes (`assets/q3_clusters.png`), et rapport textuel des profils.
* **À envoyer à** : Membre 8 (UI), Membre 9 (App) et Membre 10 (Rapport).

### 🤖 BLOC 7 : Analyste Data Science — Question 4 (Classification supervisée)
* **Membre responsable** : Membre 7
* **Outils** : Python (`scikit-learn` pour la Régression Logistique ou l'Arbre de décision).
* **Mission** : Entraîner un classifieur supervisé pour prédire l'étiquette Premium/Standard. Calculer la matrice de confusion, l'accuracy, la précision et la sensibilité (recall). Expliquer à la fondatrice les risques et coûts commerciaux des faux positifs (dilution de la marque) et des faux négatifs (départ de bons freelances).
* **Livrable** : Code d'entraînement, graphique de la matrice de confusion (`assets/q4_matrix.png`), et analyse textuelle d'évaluation des risques business.
* **À envoyer à** : Membre 8 (UI), Membre 9 (App) et Membre 10 (Rapport).

### 🎨 BLOC 8 : Développeur Front / UI — Visualisation & Interface Web
* **Membre responsable** : Membre 8
* **Outils** : Python, framework `streamlit` pour une interface Web interactive et moderne.
* **Mission** : Créer l'interface utilisateur de l'application. Organiser les affichages par onglets ou pages pour présenter de manière fluide les résultats et les visualisations interactives.
* **Livrable** : Le fichier d'interface `src/app_ui.py` avec un design premium et structuré.
* **À envoyer à** : Membre 9 (pour l'intégration).

### 🛠️ BLOC 9 : Intégrateur Dev — Packaging Application & Exécution
* **Membre responsable** : Membre 9
* **Outils** : Python, gestion d'environnement virtuel.
* **Mission** : Assembler le code de génération de données (M3), des analyses mathématiques (M4, M5, M6, M7) et de l'interface Streamlit (M8) dans un script final unifié (`src/app.py`). S'assurer de l'intégration correcte du fichier de données CSV.
* **Livrable** : Fichier final d'application `src/app.py` testé et sans bogues, prêt à être exécuté.
* **À envoyer à** : Membre 10 (pour packaging final).

### ✍️ BLOC 10 : Éditeur en Chef — Assemblage & Compilation du Rapport
* **Membre responsable** : Membre 10 (Éditeur final)
* **Outils** : LaTeX, Google Docs ou Word (Export au format final **PDF**).
* **Mission** : Collecter l'ensemble des textes, équations et figures produits par les membres 1, 2, 4, 5, 6, 7. Rédiger l'introduction, la phrase obligatoire justifiant l'utilisation de Python pour ce TP, et assembler le document complet "Rapport". Récupérer les codes sources du Membre 9. Fusionner le tout dans un dossier nommé **`INF232_TP_GROUPE01`**, compresser en `.zip` et soumettre le livrable final sur Google Form avant l'heure limite (**Dimanche 23h59**).
* **Livrable** : Fichier PDF final `Rapport.pdf` à la racine et dépôt de l'archive ZIP.

---

## 📂 Organisation de l'arbre de fichiers du dépôt

```text
INF232_TP_GROUPE01/
├── data/
│   └── freelances_data.csv       <-- Généré par le Membre 3 (Fait ✅)
├── src/
│   ├── graine.py                 <-- Code du Membre 1 (Fait ✅)
│   ├── generate_data.py          <-- Code du Membre 3 (Fait ✅)
│   ├── analysis_q1.py            <-- Code du Membre 4 (à venir)
│   ├── analysis_q2.py            <-- Code du Membre 5 (Fait ✅)
│   ├── analysis_q3.py            <-- Code du Membre 6 (à venir)
│   ├── analysis_q4.py            <-- Code du Membre 7 (à venir)
│   └── app.py                    <-- Code d'intégration final Streamlit (M9 - à venir)
├── assets/
│   ├── q1_boxplot.png            <-- Graphique de performance du Membre 4 (à venir)
│   ├── q2_regression.png         <-- Graphique de régression du Membre 5 (Fait ✅)
│   ├── q3_clusters.png           <-- Graphique de clustering du Membre 6 (à venir)
│   └── q4_matrix.png             <-- Graphique de classification du Membre 7 (à venir)
├── text_sections/
│   ├── justification_graine.md   <-- Justification de la graine du Membre 1 (Fait ✅)
│   ├── m2_justification.md       <-- Justification de la modélisation du Membre 2 (Fait ✅)
│   ├── q2_analysis.md            <-- Analyse de la régression du Membre 5 (Fait ✅)
│   └── ...                       <-- Sections rédigées par les autres membres (à venir)
├── README.md                     <-- Ce fichier de coordination et notice (Fait ✅)
└── Rapport.pdf                   <-- Rapport PDF final assemblé par le Membre 10 (à venir)
```
