# Question 1 : Analyse descriptive de la performance (Membre 4: NGONO DANIELLE STEPHANIE ESTELLE)

## A. Méthodes mobilisées et justification

Pour la première question, nous utilisons une analyse univariée de la variable `score_performance` avec Python, pandas, matplotlib et seaborn. Les calculs statistiques incluent la moyenne, la médiane, la variance et l'écart-type. La détection d'outliers s'appuie sur la méthode de l'IQR (Interquartile Range) et la boîte à moustaches de Tukey pour identifier les freelances dont la performance est statistiquement atypique.

## B. Résultats et calculs statistiques

- Moyenne de la performance : valeur centrale de l'échantillon.
- Médiane de la performance : valeur médiane qui sépare les 50 % des freelances les mieux notés.
- Variance : dispersion des scores autour de la moyenne.
- Écart-type : mesure de la volatilité de la performance dans l'échantillon.
- Outiers IQR : freelances dont le score de performance se situe en dehors de l'intervalle [Q1 - 1,5 × IQR, Q3 + 1,5 × IQR].

## C. Synthèse à destination du comité d'investisseurs

L'analyse de la performance montre la qualité générale du fichier de freelances . Une moyenne élevée indique que la majorité des freelances ont des scores performants, tandis que la médiane conforte cette observation en limitant l'influence des valeurs extrêmes. Pour les investisseurs, cela signifie que la base de talents est globalement solide et que la plateforme peut raisonnablement proposer des freelances compétents à ses clients.

La présence d'outiers identifiés par la boîte à moustaches est aussi utile : elle permet de repérer les profils très en dessous ou très au-dessus de la tendance générale. Ces freelances peuvent être traités différemment dans les stratégies commerciales : les meilleurs peuvent être mis en avant dans une offre Premium, et les moins performants peuvent nécessiter un accompagnement ou une vérification de qualité.

## D. Analyse critique et limites

La principale limite de cette analyse est qu'elle porte uniquement sur le `score_performance` et ne tient pas compte des autres dimensions importantes du modèle économique, telles que le TJM, l'expérience client, le domaine d'expertise ou la régularité des missions. Un score de performance élevé peut masquer des disparités dans la spécialisation ou la capacité à livrer sur des projets complexes.

Par ailleurs, la méthode IQR identifie les valeurs atypiques, mais elle ne distingue pas les outliers pertinents des anomalies liées à des erreurs de saisie. Une performance très basse ou très haute peut être due à un artefact du jeu de données plutôt qu'à un réel comportement commercial.

Enfin, l'échantillon étant généré de manière déterministe et synthétique, il reflète davantage la structure choisie par le groupe que la variabilité d'un marché freelance réel. Les décisions d'investissement doivent donc être prises en gardant à l'esprit que les résultats sont illustratifs et qu'une validation sur des données opérationnelles réelles reste nécessaire.
