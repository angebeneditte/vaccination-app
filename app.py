import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Configuration de la page
st.set_page_config(
    page_title="VaxData | Collecte & Analyse",
    page_icon="🏥",
    layout="wide"
)

# Icône de secours (Lien direct valide vers une icône de santé)
ICON_URL = "https://cdn-icons-png.flaticon.com/512/2966/2966486.png"

# 2. Barre latérale (Sidebar) avec un peu plus de style
with st.sidebar:
    st.image(ICON_URL, width=100)
    st.title("Système VaxData")
    st.markdown("---")
    page = st.radio(
        "Navigation",
        ["Accueil", "Enregistrement", "📊 Dashboard Analyse"],
        index=0
    )
    st.sidebar.markdown("---")
    st.sidebar.caption("© 2026 - Plateforme de Santé Infantile")

# --- Initialisation du CSV (Automatique et robuste) ---
CSV_FILE = 'data.csv'

# 3. Page d'Accueil
if page == "Accueil":
    st.title("🛡️ Bienvenue sur VaxData")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.info("### Mission de l'application")
        st.write("""
        Cette plateforme universitaire est dédiée à la collecte et à l'analyse descriptive des données de vaccination 
        pour les enfants âgés de **0 à 10 ans**.
        
        **Comment utiliser l'app :**
        1. Allez dans l'onglet **Enregistrement** pour saisir un nouvel acte médical.
        2. Consultez le **Dashboard** pour visualiser les statistiques en temps réel.
        """)
    with col2:
        st.image(ICON_URL, caption="Santé & Vaccination")

# 4. Page de Collecte (CSV Inclus)
elif page == "Enregistrement":
    st.header("Collecte des Données")
    
    with st.form("main_form", clear_on_submit=True):
        st.markdown("#### Informations de l'enfant")
        c1, c2 = st.columns(2)
        with c1:
            nom = st.text_input("Nom complet")
            age = st.number_input("Âge (0-10 ans)", 0, 10)
        with c2:
            vaccin = st.selectbox("Vaccin", ["BCG", "Polio", "DTC", "Rougeole", "Hépatite B"])
            date_v = st.date_input("Date")

        st.markdown("#### Localisation et Contexte")
        c3, c4 = st.columns(2)
        with c3:
            region = st.selectbox("Région", ["Centre", "Littoral", "Nord", "Ouest", "Est", "Sud"])
            ville = st.text_input("Ville")
        with c4:
            contexte = st.radio("Type de lieu", ["Hôpital", "Campagne mobile"], horizontal=True)

        submitted = st.form_submit_button("Enregistrer les données")
        
        if submitted:
            if nom and ville:
                new_data = {
                    "Nom": nom, "Age": age, "Vaccin": vaccin, 
                    "Date": str(date_v), "Region": region, 
                    "Ville": ville, "Lieu": contexte
                }
                df = pd.DataFrame([new_data])
                # Sauvegarde CSV
                df.to_csv(CSV_FILE, mode='a', index=False, header=not os.path.exists(CSV_FILE))
                st.success(f"✅ Donnée enregistrée pour {nom}")
                st.balloons()
            else:
                st.error("⚠️ Veuillez remplir le nom et la ville.")

# 5. Page Dashboard (Couleurs et Graphes)
elif page == "📊 Dashboard Analyse":
    st.header("📊 Dashboard Décisionnel")

    if os.path.exists(CSV_FILE):
        df_load = pd.read_csv(CSV_FILE)
        
        # --- Section Colorée (KPIs) ---
        st.markdown("### 📈 Indicateurs clés")
        k1, k2, k3 = st.columns(3)
        k1.container().metric("Total Enfants", len(df_load))
        k2.container().metric("Villes couvertes", df_load['Ville'].nunique())
        k3.container().metric("Âge Moyen", round(df_load['Age'].mean(), 1))

        st.markdown("---")
        
        # --- Graphiques ---
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("Répartition par Région")
            fig1 = px.bar(df_load['Region'].value_counts(), 
                         color_discrete_sequence=['#2E7D32'], # Vert
                         labels={'index': 'Région', 'value': 'Nombre'})
            st.plotly_chart(fig1, use_container_width=True)

        with col_right:
            st.subheader("Répartition des Lieux")
            fig2 = px.pie(df_load, names='Lieu', 
                         color_discrete_sequence=['#004d99', '#2E7D32']) # Bleu et Vert
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Histogramme des Âges")
        fig3 = px.histogram(df_load, x="Age", nbins=10, 
                            color_discrete_sequence=['#004d99']) # Bleu
        st.plotly_chart(fig3, use_container_width=True)

    else:
        st.warning("ℹ️ Aucune donnée disponible. Le fichier CSV sera créé après votre premier enregistrement.")
