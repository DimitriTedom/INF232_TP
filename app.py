"""
INF232 - TP Statistiques et Analyse de Données
Theme B : Plateforme Freelance/Client
BLOC 9 : Intégration Finale - Application Unifiée (Membre 9)

Cette application fusionne la structure de l'interface utilisateur du Membre 8
avec les algorithmes de calcul et de modélisation des Membres 3 à 7.

Note de conception : Étant donné que le système cible est hors-ligne et ne dispose
pas de matplotlib ni de seaborn, les visualisations ont été entièrement réécrites
avec Plotly (Express et Graph Objects) pour garantir un fonctionnement sans plantage
et offrir une interactivité beaucoup plus moderne (survol des données, zoom, etc.).
"""

from __future__ import annotations

import pathlib
import textwrap
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    r2_score,
    recall_score,
    precision_score,
    silhouette_score,
)
from sklearn.model_selection import train_test_split

# ---------------------------------------------------------------------------
# 0. DESIGN TOKENS (Identiques au Membre 8)
# ---------------------------------------------------------------------------
COULEUR_CANVAS = "#F5F7FA"
COULEUR_CARTE = "#FFFFFF"
COULEUR_BORDURE = "#E4E7EC"
COULEUR_ENCRE = "#101828"
COULEUR_TEXTE_ATTENUE = "#64748B"
COULEUR_MARQUE = "#0F6B62"

ACCENT_Q1 = "#0F6B62"  # teal   — Statistique descriptive
ACCENT_Q2 = "#C99A3D"  # or     — Régression
ACCENT_Q3 = "#5B5F97"  # indigo — Clustering
ACCENT_Q4 = "#B4463A"  # brique — Classification (signal de risque business)

POLICE_TITRE = "'Space Grotesk', sans-serif"
POLICE_TEXTE = "'Inter', sans-serif"
POLICE_DONNEES = "'IBM Plex Mono', monospace"

# ---------------------------------------------------------------------------
# 1. CONFIGURATION ET INJECTION CSS (Identiques au Membre 8)
# ---------------------------------------------------------------------------
def injecter_css() -> None:
    """Injecte les tokens de design (polices, couleurs, cartes) dans la page."""
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

        html, body, [class*="css"] {{
            font-family: {POLICE_TEXTE};
            color: {COULEUR_ENCRE};
        }}
        .stApp {{
            background-color: {COULEUR_CANVAS};
        }}
        h1, h2, h3 {{
            font-family: {POLICE_TITRE} !important;
            letter-spacing: -0.01em;
        }}
        [data-testid="stSidebar"] {{
            background-color: {COULEUR_ENCRE};
        }}
        [data-testid="stSidebar"] * {{
            color: #E4E7EC !important;
        }}
        [data-testid="stSidebar"] hr {{
            border-color: #2A3441;
        }}

        /* Onglets : style "pilule" plus affirmé que le style Streamlit par defaut */
        button[data-baseweb="tab"] {{
            font-family: {POLICE_TITRE};
            font-weight: 600;
            font-size: 15px;
        }}
        button[data-baseweb="tab"][aria-selected="true"] {{
            color: {COULEUR_MARQUE} !important;
        }}
        [data-baseweb="tab-highlight"] {{
            background-color: {COULEUR_MARQUE} !important;
        }}

        .carte-metrique {{
            background: {COULEUR_CARTE};
            border: 1px solid {COULEUR_BORDURE};
            border-radius: 10px;
            padding: 14px 18px;
            height: 100%;
            margin-bottom: 12px;
        }}
        .carte-metrique .label {{
            font-family: {POLICE_DONNEES};
            font-size: 11.5px;
            color: {COULEUR_TEXTE_ATTENUE};
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }}
        .carte-metrique .valeur {{
            font-family: {POLICE_TITRE};
            font-size: 26px;
            font-weight: 600;
            color: {COULEUR_ENCRE};
            margin-top: 2px;
        }}

        .badge-genere {{
            display: inline-block;
            font-family: {POLICE_DONNEES};
            font-size: 11.5px;
            color: {COULEUR_TEXTE_ATTENUE};
            background: {COULEUR_CANVAS};
            border: 1px solid {COULEUR_BORDURE};
            border-radius: 6px;
            padding: 3px 9px;
            margin-top: 6px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def carte_metrique(label: str, valeur: str, accent: str) -> str:
    """Construit le HTML d'une carte de métrique à bordure colorée par section."""
    return f"""
    <div class="carte-metrique" style="border-left: 4px solid {accent};">
        <div class="label">{label}</div>
        <div class="valeur">{valeur}</div>
    </div>
    """

def conteneur_carte():
    """st.container avec support de bordure."""
    try:
        return st.container(border=True)
    except TypeError:
        return st.container()

# Configuration des chemins
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "freelances_data.csv"
TEXT_DIR = BASE_DIR / "text_sections"
SEED_GROUPE = 853155114

# Appliquer le style CSS
injecter_css()

# ---------------------------------------------------------------------------
# 2. CHARGEMENT ET GÉNÉRATION DE DONNÉES
# ---------------------------------------------------------------------------
@st.cache_data
def charger_donnees() -> pd.DataFrame:
    """Charge le CSV. S'il n'existe pas, recrée le jeu de données du Membre 3."""
    if DATA_PATH.exists():
        return pd.read_csv(DATA_PATH)
        
    # Algorithme de génération du Membre 3 (Graine 853155114)
    rng = np.random.default_rng(SEED_GROUPE)
    N = 250
    TJM_MIN, TJM_MAX = 100, 950
    PERF_MIN, PERF_MAX = 0, 100
    N_OUTLIERS = 8
    
    qualite = rng.normal(loc=0.0, scale=1.0, size=N)
    
    tjm_base = rng.gamma(shape=2.2, scale=140, size=N)
    tjm_bruit = rng.normal(0, 60, size=N)
    tjm_brut = tjm_base + 90 * qualite + tjm_bruit
    tjm_scaled = (tjm_brut - tjm_brut.min()) / (tjm_brut.max() - tjm_brut.min())
    tjm = TJM_MIN + tjm_scaled * (TJM_MAX - TJM_MIN)
    
    perf_bruit = rng.normal(0, 12, size=N)
    perf_brut = 55 + 14 * qualite + perf_bruit
    performance = np.clip(perf_brut, PERF_MIN, PERF_MAX)
    performance = np.round(performance).astype(int)
    
    outlier_idx = rng.choice(N, size=N_OUTLIERS, replace=False)
    for i in outlier_idx:
        if rng.random() < 0.5:
            tjm[i] = TJM_MIN if rng.random() < 0.5 else TJM_MAX - rng.uniform(0, 10)
        else:
            performance[i] = PERF_MIN if rng.random() < 0.5 else PERF_MAX
            
    tjm = np.round(tjm, 1)
    
    tjm_norm = (tjm - tjm.min()) / (tjm.max() - tjm.min())
    perf_norm = (performance - performance.min()) / (performance.max() - performance.min())
    score_composite = 0.55 * tjm_norm + 0.45 * perf_norm
    seuil = np.quantile(score_composite, 0.78)
    proba_premium = 1 / (1 + np.exp(-10 * (score_composite - seuil)))
    
    tirage = rng.random(N)
    statut = np.where(tirage < proba_premium, "Premium", "Standard")
    
    df = pd.DataFrame({
        "id_freelance": np.arange(1, N + 1),
        "tjm_euros": tjm,
        "score_performance": performance,
        "statut": statut,
    })
    
    # Exporter le fichier créé
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_PATH, index=False, encoding="utf-8")
    return df

df = charger_donnees()

# ---------------------------------------------------------------------------
# 3. TRACÉS INTERACTIFS PLOTLY (Calculs unifiés des Membres 4 à 7)
# ---------------------------------------------------------------------------
def generer_q1_boxplot(df: pd.DataFrame):
    """Reproduit le boxplot du Membre 4."""
    fig = px.box(
        df,
        x="score_performance",
        color_discrete_sequence=[ACCENT_Q1],
        labels={"score_performance": "Score de Performance"}
    )
    fig.update_layout(
        title="Boîte à moustaches du score de performance",
        title_font=dict(family="Space Grotesk", size=16, color=COULEUR_ENCRE),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=True, gridcolor=COULEUR_BORDURE),
        font_family="Inter",
        height=320
    )
    return fig

def generer_q2_regression(df: pd.DataFrame):
    """Reproduit la régression linéaire du Membre 5 sur le TJM en Euros."""
    X_r = df[["tjm_euros"]]
    y_r = df["score_performance"]

    modele = LinearRegression()
    modele.fit(X_r, y_r)
    y_pred = modele.predict(X_r)
    r2 = r2_score(y_r, y_pred)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["tjm_euros"], y=df["score_performance"],
        mode='markers', name='Freelances',
        marker=dict(color='#2b5c8f', opacity=0.7, size=6)
    ))
    
    # Sort values for smooth line
    sorted_indices = np.argsort(df["tjm_euros"])
    fig.add_trace(go.Scatter(
        x=df["tjm_euros"].iloc[sorted_indices],
        y=y_pred[sorted_indices],
        mode='lines', name=f'Droite de régression (R² = {r2:.3f})',
        line=dict(color=ACCENT_Q2, width=2.5)
    ))

    fig.update_layout(
        title="Relation entre le TJM (€) et la Performance",
        title_font=dict(family="Space Grotesk", size=16, color=COULEUR_ENCRE),
        xaxis_title="Taux Journalier Moyen (en €)",
        yaxis_title="Score de Performance (sur 100)",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=True, gridcolor=COULEUR_BORDURE),
        yaxis=dict(showgrid=True, gridcolor=COULEUR_BORDURE),
        font_family="Inter",
        legend=dict(x=0.02, y=0.98),
        height=400
    )
    return fig

def generer_q3_clustering(df: pd.DataFrame, k: int):
    """Reproduit le clustering K-Means du Membre 6 avec choix interactif de K."""
    features = ["tjm_euros", "score_performance"]
    X = df[features].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans_final = KMeans(n_clusters=k, n_init=10, random_state=SEED_GROUPE)
    clusters = kmeans_final.fit_predict(X_scaled)
    centroids_original = scaler.inverse_transform(kmeans_final.cluster_centers_)
    
    # Silhouette score
    sil_score = silhouette_score(X_scaled, clusters)

    df_plot = df.copy()
    df_plot["cluster"] = clusters
    df_plot["cluster_str"] = df_plot["cluster"].apply(lambda c: f"Cluster {c}")

    fig = px.scatter(
        df_plot, x="tjm_euros", y="score_performance",
        color="cluster_str",
        labels={"tjm_euros": "TJM (€)", "score_performance": "Score Performance"},
        color_discrete_sequence=px.colors.qualitative.T10
    )
    
    fig.add_trace(go.Scatter(
        x=centroids_original[:, 0], y=centroids_original[:, 1],
        mode='markers', name='Centroïdes',
        marker=dict(symbol='x', size=12, color='black', line=dict(width=1.5, color='white'))
    ))

    fig.update_layout(
        title=f"Clusters K-Means (K={k} | Silhouette = {sil_score:.3f})",
        title_font=dict(family="Space Grotesk", size=16, color=COULEUR_ENCRE),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=True, gridcolor=COULEUR_BORDURE),
        yaxis=dict(showgrid=True, gridcolor=COULEUR_BORDURE),
        font_family="Inter",
        height=400
    )

    return fig, sil_score, df_plot

def generer_q4_matrice_confusion(df: pd.DataFrame):
    """Reproduit la classification logistique du Membre 7."""
    features = ["tjm_euros", "score_performance"]
    X = df[features]
    y = (df["statut"] == "Premium").astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=SEED_GROUPE, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    modele = LogisticRegression(random_state=SEED_GROUPE)
    modele.fit(X_train_scaled, y_train)
    y_pred = modele.predict(X_test_scaled)

    accuracy = accuracy_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    matrice = confusion_matrix(y_test, y_pred)

    fig = px.imshow(
        matrice, text_auto=True,
        labels=dict(x="Statut Prédit", y="Statut Réel"),
        x=['Standard', 'Premium'],
        y=['Standard', 'Premium'],
        color_continuous_scale=[[0, '#ffffff'], [1, ACCENT_Q4]]
    )
    
    fig.update_layout(
        title=f"Matrice de confusion (Accuracy = {accuracy:.1%})",
        title_font=dict(family="Space Grotesk", size=16, color=COULEUR_ENCRE),
        coloraxis_showscale=False,
        width=360, height=360,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_family="Inter"
    )

    return fig, accuracy, recall, precision, modele, scaler

# ---------------------------------------------------------------------------
# 4. CHARGEMENT DU TEXTE D'ANALYSE
# ---------------------------------------------------------------------------
def afficher_texte_si_disponible(nom_fichier: str, membre: str) -> None:
    """Affiche un texte Markdown de text_sections/ dans un expander."""
    chemin = TEXT_DIR / nom_fichier
    with st.expander("📖 Lecture business", expanded=False):
        if chemin.exists() and chemin.read_text(encoding="utf-8").strip():
            st.markdown(chemin.read_text(encoding="utf-8"))
        else:
            st.info(
                f"📌 Analyse textuelle en attente : `{nom_fichier}` sera rédigée par le **{membre}**."
            )

# ---------------------------------------------------------------------------
# 5. CONFIGURATION BARRE LATÉRALE
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        f"""
        <div style="font-family:{POLICE_TITRE}; font-size:21px; font-weight:700; color:white;">
            💼 Freelance Analytics
        </div>
        <div style="font-family:{POLICE_TEXTE}; font-size:13px; color:#9AA4B2; margin-top:2px;">
            INF232 — Statistiques et Analyse de Données
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")

    st.markdown("**ℹ️ À propos du projet**")
    st.caption(
        "Exploration et modélisation statistique d'un jeu de données de "
        "freelances (TJM, performance, statut Premium/Standard)."
    )

    st.markdown("---")
    st.markdown("**🔑 Reproductibilité**")
    st.markdown(
        f'<span style="font-family:{POLICE_DONNEES}; font-size:12.5px; '
        f'background:#1C2530; border:1px solid #2A3441; border-radius:6px; '
        f'padding:4px 8px; color:#7ee787;">graine = {SEED_GROUPE}</span>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("**👥 Groupe 14 — Thème B**")
    st.caption(
        "M1 Coordination · M2 Modélisation · M3 Génération · "
        "M4 Q1 · M5 Q2 · M6 Q3 · M7 Q4 · M8 UI · M9 Intégration · M10 Rapport"
    )
    
    # Quick Action to regenerate CSV data
    if st.sidebar.button("🔄 Régénérer données (M3)"):
        st.cache_data.clear()
        if DATA_PATH.exists():
            DATA_PATH.unlink()
        df = charger_donnees()
        st.sidebar.success("Données régénérées avec succès !")

# ---------------------------------------------------------------------------
# 6. STRUCTURE PRINCIPALE EN ONGLETS
# ---------------------------------------------------------------------------
onglet_intro, onglet_q1, onglet_q2, onglet_q3, onglet_q4 = st.tabs(
    [
        "🏠 Introduction",
        "📈 Statistique Descriptive",
        "📉 Régression",
        "🧩 Clustering",
        "🎯 Classification",
    ]
)

# ---------------------------------------------------------------------------
# ONGLET 1 : INTRODUCTION
# ---------------------------------------------------------------------------
with onglet_intro:
    n_freelances = len(df)
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, {COULEUR_MARQUE} 0%, #0B4941 100%);
                    border-radius: 14px; padding: 34px 38px; margin-bottom: 22px;">
            <div style="font-family:{POLICE_DONNEES}; font-size:12.5px; color:#BFE3DB;
                        text-transform:uppercase; letter-spacing:0.08em;">Groupe 14 · Thème B</div>
            <div style="font-family:{POLICE_TITRE}; font-size:38px; font-weight:700; color:white; margin-top:6px;">
                {n_freelances} freelances analysés
            </div>
            <div style="font-family:{POLICE_TEXTE}; font-size:15px; color:#D7ECE7; margin-top:8px; max-width:640px;">
                Plateforme freelance/client — TJM, score de performance et statut commercial (Premium / Standard),
                explorés sous quatre angles statistiques complémentaires.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    intro_texte = textwrap.dedent(
        """
        L'objectif est d'explorer ces données sous quatre angles complémentaires :
        - **Statistique descriptive univariée** (Question 1)
        - **Corrélation et régression linéaire** (Question 2)
        - **Segmentation non supervisée (K-Means)** (Question 3)
        - **Classification supervisée (Régression Logistique)** (Question 4)
        """
    )
    st.markdown(intro_texte)

    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(carte_metrique("TJM moyen", f"{df['tjm_euros'].mean():.0f} €", ACCENT_Q1), unsafe_allow_html=True)
    col2.markdown(carte_metrique("Performance moyenne", f"{df['score_performance'].mean():.1f}/100", ACCENT_Q2), unsafe_allow_html=True)
    part_premium = (df["statut"] == "Premium").mean() * 100
    col3.markdown(carte_metrique("Part Premium", f"{part_premium:.1f} %", ACCENT_Q3), unsafe_allow_html=True)
    col4.markdown(carte_metrique("Freelances", f"{len(df)}", ACCENT_Q4), unsafe_allow_html=True)

    st.markdown("####")
    st.markdown("**Aperçu des 10 premières lignes**")
    st.dataframe(df.head(10), use_container_width=True)

# ---------------------------------------------------------------------------
# ONGLET 2 : STATISTIQUE DESCRIPTIVE (Q1 - Membre 4)
# ---------------------------------------------------------------------------
with onglet_q1:
    st.header("Question 1 — Statistique Descriptive Univariée")
    st.caption("Analyse : Membre 4 · Variable étudiée : score de performance")

    perf = df["score_performance"]
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(carte_metrique("Moyenne", f"{perf.mean():.2f}", ACCENT_Q1), unsafe_allow_html=True)
    col2.markdown(carte_metrique("Médiane", f"{perf.median():.2f}", ACCENT_Q1), unsafe_allow_html=True)
    col3.markdown(carte_metrique("Variance", f"{perf.var(ddof=1):.2f}", ACCENT_Q1), unsafe_allow_html=True)
    col4.markdown(carte_metrique("Écart-type", f"{perf.std(ddof=1):.2f}", ACCENT_Q1), unsafe_allow_html=True)
    st.markdown("####")

    col_plot, col_outliers = st.columns([3, 2])
    with col_plot:
        with conteneur_carte():
            fig_q1 = generer_q1_boxplot(df)
            st.plotly_chart(fig_q1, use_container_width=True)
            
    with col_outliers:
        Q1 = perf.quantile(0.25)
        Q3 = perf.quantile(0.75)
        IQR = Q3 - Q1
        borne_inf = Q1 - 1.5 * IQR
        borne_sup = Q3 + 1.5 * IQR
        outliers = df[(perf < borne_inf) | (perf > borne_sup)]
        
        st.markdown(f"**Détection d'Outliers (Tukey IQR)**")
        st.write(f"Intervalle de confiance : `[{borne_inf:.1f}, {borne_sup:.1f}]`")
        st.write(f"Nombre de profils atypiques détectés : `{len(outliers)}` sur {len(df)}")
        if len(outliers) > 0:
            st.dataframe(outliers[["id_freelance", "tjm_euros", "score_performance", "statut"]], height=180, use_container_width=True)

    afficher_texte_si_disponible("q1_analysis.md", "Membre 4")

# ---------------------------------------------------------------------------
# ONGLET 3 : RÉGRESSION (Q2 - Membre 5)
# ---------------------------------------------------------------------------
with onglet_q2:
    st.header("Question 2 — Corrélation et Régression Linéaire")
    st.caption("Analyse : Membre 5 · TJM (X) vs Score de performance (Y)")

    col1, col2 = st.columns(2)
    col1.markdown(carte_metrique("Corrélation de Pearson", f"{df['tjm_euros'].corr(df['score_performance'], method='pearson'):.3f}", ACCENT_Q2), unsafe_allow_html=True)
    col2.markdown(carte_metrique("Corrélation de Spearman", f"{df['tjm_euros'].corr(df['score_performance'], method='spearman'):.3f}", ACCENT_Q2), unsafe_allow_html=True)
    st.markdown("####")

    col_plot, col_pred = st.columns([3, 2])
    with col_plot:
        with conteneur_carte():
            fig_q2 = generer_q2_regression(df)
            st.plotly_chart(fig_q2, use_container_width=True)
            
    with col_pred:
        st.markdown("#### 🧮 Estimateur de Performance en Direct")
        st.write("Ajustez le TJM pour estimer en direct le score de performance d'un nouveau freelance :")
        sim_tjm = st.slider("TJM du Freelance (en euros)", min_value=100, max_value=950, value=350, step=10)
        
        # Fit model on the fly for prediction
        modele_lin = LinearRegression()
        modele_lin.fit(df[["tjm_euros"]], df["score_performance"])
        predicted_perf = modele_lin.predict([[sim_tjm]])[0]
        predicted_perf_clipped = np.clip(predicted_perf, 0, 100)
        
        st.metric(
            label="Score de Performance Estimé",
            value=f"{predicted_perf_clipped:.2f} / 100",
            delta=f"{(predicted_perf_clipped - df['score_performance'].mean()):+.2f} vs Moyenne"
        )
        st.progress(int(predicted_perf_clipped))

    afficher_texte_si_disponible("q2_analysis.md", "Membre 5")

# ---------------------------------------------------------------------------
# ONGLET 4 : CLUSTERING (Q3 - Membre 6)
# ---------------------------------------------------------------------------
with onglet_q3:
    st.header("Question 3 — Segmentation non supervisée (K-Means)")
    st.caption("Analyse : Membre 6 · Variables standardisées : TJM, score de performance")

    col_ctrl, col_plot = st.columns([2, 3])
    with col_ctrl:
        st.markdown("#### ⚙️ Configuration de K-Means")
        st.write("Ajustez K en direct pour observer la réorganisation des profils :")
        k_selected = st.slider("Nombre de clusters (K)", min_value=2, max_value=8, value=2, step=1)
        
        # Run live clustering
        fig_q3, silhouette, df_clustered = generer_q3_clustering(df, k_selected)
        
        st.markdown(f"**Score de Silhouette actuel** : `{silhouette:.3f}`")
        
        # Cluster Profile Summary Table
        profils = df_clustered.groupby("cluster_str").agg(
            effectif=("tjm_euros", "count"),
            tjm_moyen=("tjm_euros", "mean"),
            perf_moyenne=("score_performance", "mean")
        ).reset_index()
        
        st.markdown("**Profils par cluster :**")
        st.dataframe(profils.style.format({
            "tjm_moyen": "{:.1f} €",
            "perf_moyenne": "{:.1f}/100"
        }), use_container_width=True)

    with col_plot:
        with conteneur_carte():
            st.plotly_chart(fig_q3, use_container_width=True)
            
    # Cross tabulation display
    st.markdown("#### ⚖️ Recoupement a posteriori avec la segmentation commerciale")
    cross_tab = pd.crosstab(df_clustered["cluster_str"], df_clustered["statut"])
    st.table(cross_tab)

    afficher_texte_si_disponible("q3_analysis.md", "Membre 6")

# ---------------------------------------------------------------------------
# ONGLET 5 : CLASSIFICATION (Q4 - Membre 7)
# ---------------------------------------------------------------------------
with onglet_q4:
    st.header("Question 4 — Classification Supervisée (Régression Logistique)")
    st.caption("Analyse : Membre 7 · Prédiction du statut Premium / Standard")

    fig_q4, acc, recall, precision, model_cls, scaler_cls = generer_q4_matrice_confusion(df)

    col_plot, col_pred = st.columns([1, 1])
    with col_plot:
        col_m1, col_m2 = st.columns(2)
        col_m1.markdown(carte_metrique("Accuracy (Précision globale)", f"{acc:.2%}", ACCENT_Q4), unsafe_allow_html=True)
        col_m2.markdown(carte_metrique("Rappel Premium (Recall)", f"{recall:.2%}", ACCENT_Q4), unsafe_allow_html=True)
        st.markdown("####")
        with conteneur_carte():
            st.plotly_chart(fig_q4, use_container_width=True)
            
    with col_pred:
        st.markdown("#### 🔮 Prédicteur de Statut Commercial en Temps Réel")
        st.write("Saisissez le profil d'un nouveau freelance pour prédire son éligibilité au statut Premium :")
        input_tjm = st.number_input("Taux Journalier Moyen (€)", min_value=100.0, max_value=950.0, value=350.0, step=10.0)
        input_perf = st.slider("Score de Performance (0-100)", min_value=0, max_value=100, value=65)
        
        # Scale and predict
        input_scaled = scaler_cls.transform([[input_tjm, input_perf]])
        pred_label = model_cls.predict(input_scaled)[0]
        pred_proba = model_cls.predict_proba(input_scaled)[0]
        
        st.markdown("<br>", unsafe_allow_html=True)
        if pred_label == 1:
            st.markdown(f"**Classe prédite** : <span class='badge-genere' style='color:#ffffff; background:{ACCENT_Q1}; border-color:{ACCENT_Q1};'>Premium</span>", unsafe_allow_html=True)
            st.info(f"Probabilité d'être Premium : **{pred_proba[1]*100:.1f} %**")
        else:
            st.markdown(f"**Classe prédite** : <span class='badge-genere' style='color:#ffffff; background:{ACCENT_Q4}; border-color:{ACCENT_Q4};'>Standard</span>", unsafe_allow_html=True)
            st.warning(f"Probabilité d'être Premium : **{pred_proba[1]*100:.1f} %** (Seuil requis > 50%)")

    afficher_texte_si_disponible("q4_analysis.md", "Membre 7")

# ---------------------------------------------------------------------------
# 8. PIED DE PAGE
# ---------------------------------------------------------------------------
st.markdown("---")
st.caption(
    "INF232 — Groupe 14 · Thème B (Plateforme Freelance/Client) · "
    "Intégration unifiée et finale UI/Calculs (Membre 9) — "
    "Moteur de visualisation interactif Plotly opérationnel."
)
