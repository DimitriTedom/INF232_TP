"""
INF232 - TP Statistiques et Analyse de Données
Theme B : Plateforme Freelance/Client
BLOC 8 + BLOC 9 : Interface Streamlit complète (Membre 8 maquette + intégration Membre 9)

Exécution :
    streamlit run src/app.py
"""

from __future__ import annotations

import pathlib
import textwrap

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    r2_score,
    recall_score,
    silhouette_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# ---------------------------------------------------------------------------
# 0. DESIGN TOKENS (palette, typographie) — design pro pour investisseurs
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
ACCENT_Q4 = "#B4463A"  # brique — Classification (risque business)

POLICE_TITRE = "'Space Grotesk', sans-serif"
POLICE_TEXTE = "'Inter', sans-serif"
POLICE_DONNEES = "'IBM Plex Mono', monospace"

sns.set_theme(style="whitegrid")
plt.rcParams["axes.edgecolor"] = COULEUR_BORDURE
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.alpha"] = 0.35
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False


# ---------------------------------------------------------------------------
# 1. CONFIGURATION GÉNÉRALE DE LA PAGE + INJECTION CSS
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="INF232 - Plateforme Freelance/Client",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)


def injecter_css() -> None:
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
    return f"""
    <div class="carte-metrique" style="border-left: 4px solid {accent};">
        <div class="label">{label}</div>
        <div class="valeur">{valeur}</div>
    </div>
    """


def conteneur_carte():
    try:
        return st.container(border=True)
    except TypeError:
        return st.container()


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "freelances_data.csv"
ASSETS_DIR = BASE_DIR / "assets"
TEXT_DIR = BASE_DIR / "text_sections"

SEED_GROUPE = 853155114


# ---------------------------------------------------------------------------
# 2. CHARGEMENT DES DONNÉES
# ---------------------------------------------------------------------------
@st.cache_data
def charger_donnees(path: pathlib.Path) -> pd.DataFrame | None:
    if not path.exists():
        return None
    return pd.read_csv(path)


# ---------------------------------------------------------------------------
# 3. GÉNÉRATEURS DE SECOURS (si PNG absents — même logique que les analysis_q*.py)
# ---------------------------------------------------------------------------
@st.cache_data
def generer_q1_boxplot(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(x=df["score_performance"], ax=ax, color=ACCENT_Q1, width=0.35)
    ax.set_title("Boîte à moustaches du score de performance", fontweight="bold")
    ax.set_xlabel("Score de performance")
    fig.tight_layout()
    return fig


@st.cache_data
def generer_q2_regression(df: pd.DataFrame):
    X_r = df[["tjm_euros"]]
    y_r = df["score_performance"]

    modele = LinearRegression()
    modele.fit(X_r, y_r)
    y_pred = modele.predict(X_r)
    r2 = r2_score(y_r, y_pred)

    fig, ax = plt.subplots(figsize=(9, 6))
    sns.scatterplot(data=df, x="tjm_euros", y="score_performance",
                     color=ACCENT_Q1, alpha=0.65, label="Freelances", ax=ax)

    tjm_range = np.linspace(df["tjm_euros"].min(), df["tjm_euros"].max(), 100)
    tjm_range_df = pd.DataFrame({"tjm_euros": tjm_range})
    y_range_pred = modele.predict(tjm_range_df)
    ax.plot(tjm_range, y_range_pred, color=ACCENT_Q2, linewidth=2.5,
            label=f"Droite de régression (R² = {r2:.3f})")

    ax.set_title("Relation entre le TJM et la Performance", fontweight="bold")
    ax.set_xlabel("Taux Journalier Moyen (en €)")
    ax.set_ylabel("Score de Performance (sur 100)")
    ax.legend(loc="upper left")
    fig.tight_layout()
    return fig


@st.cache_data
def generer_q3_clustering(df: pd.DataFrame):
    features = ["tjm_euros", "score_performance"]
    X = df[features].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    k_range = range(2, 9)
    silhouettes = []
    for k in k_range:
        km = KMeans(n_clusters=k, n_init=10, random_state=SEED_GROUPE)
        labels_k = km.fit_predict(X_scaled)
        silhouettes.append(silhouette_score(X_scaled, labels_k))
    best_k = list(k_range)[int(np.argmax(silhouettes))]

    kmeans_final = KMeans(n_clusters=best_k, n_init=10, random_state=SEED_GROUPE)
    clusters = kmeans_final.fit_predict(X_scaled)
    centroids_original = scaler.inverse_transform(kmeans_final.cluster_centers_)

    palette_clusters = sns.light_palette(ACCENT_Q3, n_colors=best_k + 2)[2:]
    fig, ax = plt.subplots(figsize=(8, 6))
    for c in range(best_k):
        mask = clusters == c
        ax.scatter(df["tjm_euros"][mask], df["score_performance"][mask],
                   s=35, alpha=0.8, color=palette_clusters[c],
                   label=f"Cluster {c} (n={mask.sum()})")
    ax.scatter(centroids_original[:, 0], centroids_original[:, 1],
               s=250, marker="X", color=COULEUR_ENCRE, edgecolor="white",
               linewidth=1.5, label="Centroïdes", zorder=5)
    ax.set_xlabel("TJM (euros)")
    ax.set_ylabel("Score de performance")
    ax.set_title(f"Clusters K-Means (K={best_k})", fontweight="bold")
    ax.legend(fontsize=9)
    fig.tight_layout()

    return fig, best_k, silhouettes[int(np.argmax(silhouettes))]


@st.cache_data
def generer_q4_matrice_confusion(df: pd.DataFrame):
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
    matrice = confusion_matrix(y_test, y_pred)

    cmap_q4 = sns.light_palette(ACCENT_Q4, as_cmap=True)
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    sns.heatmap(matrice, annot=True, fmt="d", cmap=cmap_q4, cbar=False,
                xticklabels=["Standard", "Premium"],
                yticklabels=["Standard", "Premium"],
                annot_kws={"size": 14}, linewidths=1, linecolor="white", ax=ax)
    ax.set_title(
        f"Matrice de confusion — Régression Logistique\n"
        f"Accuracy = {accuracy:.2%} | Recall (Premium) = {recall:.2%}",
        fontweight="bold",
    )
    ax.set_xlabel("Statut prédit")
    ax.set_ylabel("Statut réel")
    fig.tight_layout()

    return fig, accuracy, recall


# ---------------------------------------------------------------------------
# 4. AFFICHAGE GRAPH + TEXTE
# ---------------------------------------------------------------------------
def afficher_graphique(nom_fichier: str, legende: str, generateur, df: pd.DataFrame) -> None:
    chemin = ASSETS_DIR / nom_fichier
    with conteneur_carte():
        if chemin.exists():
            st.image(str(chemin), caption=legende, use_container_width=True)
            return

        if df is None:
            st.warning("⚠️ Impossible de générer le graphique automatiquement : data/freelances_data.csv introuvable.")
            return

        with st.spinner("Génération automatique du graphique en cours..."):
            resultat = generateur(df)
        fig = resultat[0] if isinstance(resultat, tuple) else resultat
        st.pyplot(fig)
        st.markdown(
            f'<span class="badge-genere">⚙ généré automatiquement — {nom_fichier} absent de assets/</span>',
            unsafe_allow_html=True,
        )


def afficher_texte_si_disponible(nom_fichier: str, membre: str) -> None:
    chemin = TEXT_DIR / nom_fichier
    with st.expander("📖 Lecture business", expanded=False):
        if chemin.exists() and chemin.read_text(encoding="utf-8").strip():
            st.markdown(chemin.read_text(encoding="utf-8"))
        else:
            st.info(f"📌 Analyse textuelle en attente : `{nom_fichier}` sera rédigée par le **{membre}**.")


# ---------------------------------------------------------------------------
# 5. CSS + SIDEBAR
# ---------------------------------------------------------------------------
injecter_css()

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
    st.caption("Exploration et modélisation statistique d'un jeu de données de freelances (TJM, performance, statut Premium/Standard).")

    st.markdown("---")
    st.markdown("**🔑 Reproductibilité**")
    st.markdown(
        f'<span style="font-family:{POLICE_DONNEES}; font-size:12.5px; '
        f'background:#1C2530; border:1px solid #2A3441; border-radius:6px; '
        f'padding:4px 8px; color:#7ee787;">graine = {SEED_GROUPE}</span>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("**👥 Groupe 01 — Thème B**")
    st.caption("M1 Dimitri Tedom · M2 Mamboune Nchourupouo Basma · M3 Meli Tanga Jeeps Parvel · M4 Ngono Danielle Stephanie Estelle · M5 Kuichouo Leopold Stanislas · M6 Lambo Lekoubou Dimitri · M7 Tekeng Kamwélé Junior Cambell · M8 Nguefah zeutcha Carol junior · M9 Nkonzap Ariane · M10 Yonkoua Yann Luca")

# ---------------------------------------------------------------------------
# 6. DATA
# ---------------------------------------------------------------------------
df = charger_donnees(DATA_PATH)

# ---------------------------------------------------------------------------
# 7. ONGLETS
# ---------------------------------------------------------------------------
onglet_intro, onglet_q1, onglet_q2, onglet_q3, onglet_q4 = st.tabs(
    ["🏠 Introduction", "📈 Statistique Descriptive", "📉 Régression", "🧩 Clustering", "🎯 Classification"]
)

# ---------------------------------------------------------------------------
# ONGLET INTRO
# ---------------------------------------------------------------------------
with onglet_intro:
    n_freelances = len(df) if df is not None else "—"
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, {COULEUR_MARQUE} 0%, #0B4941 100%);
                    border-radius: 14px; padding: 34px 38px; margin-bottom: 22px;">
            <div style="font-family:{POLICE_DONNEES}; font-size:12.5px; color:#BFE3DB;
                        text-transform:uppercase; letter-spacing:0.08em;">Groupe 01 · Thème B</div>
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

    if df is not None:
        col1, col2, col3, col4 = st.columns(4)
        col1.markdown(carte_metrique("TJM moyen", f"{df['tjm_euros'].mean():.0f} €", ACCENT_Q1), unsafe_allow_html=True)
        col2.markdown(carte_metrique("Performance moyenne", f"{df['score_performance'].mean():.1f}/100", ACCENT_Q2), unsafe_allow_html=True)
        part_premium = (df["statut"] == "Premium").mean() * 100
        col3.markdown(carte_metrique("Part Premium", f"{part_premium:.1f} %", ACCENT_Q3), unsafe_allow_html=True)
        col4.markdown(carte_metrique("Freelances", f"{len(df)}", ACCENT_Q4), unsafe_allow_html=True)

        st.markdown("####")
        st.markdown("**Aperçu des 10 premières lignes**")
        st.dataframe(df.head(10), use_container_width=True)
    else:
        st.warning("⚠️ Le fichier `data/freelances_data.csv` n'a pas été trouvé. Exécutez `python src/generate_data.py`.")

# ---------------------------------------------------------------------------
# ONGLET Q1
# ---------------------------------------------------------------------------
with onglet_q1:
    st.header("Question 1 — Statistique Descriptive Univariée")
    st.caption("Analyse : Membre 4 · Variable étudiée : score de performance")

    if df is not None:
        perf = df["score_performance"]
        col1, col2, col3, col4 = st.columns(4)
        col1.markdown(carte_metrique("Moyenne", f"{perf.mean():.2f}", ACCENT_Q1), unsafe_allow_html=True)
        col2.markdown(carte_metrique("Médiane", f"{perf.median():.2f}", ACCENT_Q1), unsafe_allow_html=True)
        col3.markdown(carte_metrique("Variance", f"{perf.var(ddof=1):.2f}", ACCENT_Q1), unsafe_allow_html=True)
        col4.markdown(carte_metrique("Écart-type", f"{perf.std(ddof=1):.2f}", ACCENT_Q1), unsafe_allow_html=True)
        st.markdown("####")

    afficher_graphique("q1_boxplot.png", "Boîte à moustaches — Score de performance", generer_q1_boxplot, df)
    afficher_texte_si_disponible("q1_analysis.md", "Membre 4")

# ---------------------------------------------------------------------------
# ONGLET Q2
# ---------------------------------------------------------------------------
with onglet_q2:
    st.header("Question 2 — Corrélation et Régression Linéaire")
    st.caption("Analyse : Membre 5 · TJM (X) vs Score de performance (Y)")

    if df is not None:
        col1, col2 = st.columns(2)
        col1.markdown(carte_metrique("Corrélation de Pearson", f"{df['tjm_euros'].corr(df['score_performance'], method='pearson'):.3f}", ACCENT_Q2), unsafe_allow_html=True)
        col2.markdown(carte_metrique("Corrélation de Spearman", f"{df['tjm_euros'].corr(df['score_performance'], method='spearman'):.3f}", ACCENT_Q2), unsafe_allow_html=True)
        st.markdown("####")

    afficher_graphique("q2_regression.png", "Régression linéaire TJM → Performance", generer_q2_regression, df)
    afficher_texte_si_disponible("q2_analysis.md", "Membre 5")

# ---------------------------------------------------------------------------
# ONGLET Q3
# ---------------------------------------------------------------------------
with onglet_q3:
    st.header("Question 3 — Segmentation non supervisée (K-Means)")
    st.caption("Analyse : Membre 6 · Variables standardisées : TJM, score de performance")

    afficher_graphique("q3_clusters.png", "Clustering K-Means des freelances", generer_q3_clustering, df)
    afficher_texte_si_disponible("q3_analysis.md", "Membre 6")

# ---------------------------------------------------------------------------
# ONGLET Q4 — maintenant fonctionnel grâce au travail du Bloc 7
# ---------------------------------------------------------------------------
with onglet_q4:
    st.header("Question 4 — Classification Supervisée (Régression Logistique)")
    st.caption("Analyse : Membre 7 · Prédiction du statut Premium / Standard")

    afficher_graphique("q4_matrix.png", "Matrice de confusion — Classification Premium/Standard", generer_q4_matrice_confusion, df)
    afficher_texte_si_disponible("q4_analysis.md", "Membre 7")

# ---------------------------------------------------------------------------
# PIED DE PAGE
# ---------------------------------------------------------------------------
st.markdown("---")
st.caption(
    "INF232 — Groupe 01 · Thème B (Plateforme Freelance/Client) · "
    "Application intégrée (M8 UI + M9 packaging) · Bloc 7 Classification complété"
)
