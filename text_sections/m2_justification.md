# INF232 - Justification Théorique de la Modélisation des Données
**Auteur :** MAMBOUNE NCHOURUPOUO BASMA (Membre 2 - Architecte de Données)

Ce document définit et justifie la structure des données simulées pour notre plateforme de Freelances et Clients.

---

## 1. Définition et Justification des Variables

Dans le cadre d'une plateforme de mise en relation entre freelances et clients, trois variables clés ont été sélectionnées pour évaluer la dynamique du marché :

### A. Le Tarif Journalier Moyen (TJM)
* **Bornes :** 100 € à 950 € 
* **Justification métier :** Le TJM reflète la réalité économique du marché du freelancing. 
  * Un TJM de **100 €** correspond à des profils très juniors ou à des tâches à faible valeur ajoutée (ex: saisie de données, assistance simple).
  * Un TJM de **950 €** correspond à des experts hautement qualifiés et recherchés (ex: Architectes Cloud, Consultants en Cybersécurité, Data Scientists Seniors).
* **Nature de la variable :** Quantitative continue.

### B. Le Score de Performance
* **Bornes :** 0 à 100 
* **Justification métier :** Ce score agrège plusieurs indicateurs de satisfaction client (respect des délais, qualité du travail rendu, communication). 
  * Un score de **0** représente un échec critique ou un abandon de projet.
  * Un score de **100** représente une mission parfaite sans aucun accroc. 
* **Nature de la variable :** Quantitative discrète (ou continue selon l'arrondi).

### C. L'Étiquette (Statut du Freelance)
* **Valeurs :** Premium / Standard 
* **Justification métier :** Cette variable permet à la plateforme de segmenter son offre. Le statut **Premium** est une distinction attribuée aux meilleurs profils (qui combinent souvent un TJM éleve et un excellent score de performance). Cela permet de valoriser ces profils auprès des clients exigeants et prêts à payer plus cher.
* **Nature de la variable :** Qualitative nominale (binaire).

---

## 2. Justification de la Taille de l'Échantillon (N = 250)

Le choix de générer un échantillon de **N = 250 freelances** repose sur des critères statistiques, mathématiques et informatiques précis :

1. **Théorème Central Limite (TCL) :** En statistique, un échantillon est considéré comme suffisant pour appliquer les lois de grands nombres et la loi normale dès que $N > 30$. Avec $N = 250$, nous dépassons largement ce seuil, ce qui garantit la validité et la robustesse de nos futurs tests et modèles (comme la régression linéaire du Membre 5).
2. **Stabilité des Modèles de Data Science :** Pour le clustering (K-Means - Membre 6) et la classification (Régression Logistique - Membre 7), 250 lignes offrent assez de matière pour séparer distinctement des groupes sans risquer un "surapprentissage" (le modèle qui apprend par cœur les données au lieu de comprendre la logique globale).
3. **Performance de l'Application :** C'est une taille idéale pour être traitée instantanément en Python, tout en permettant un affichage fluide et visuel sur notre interface interactive Streamlit (Membres 8 et 9).
