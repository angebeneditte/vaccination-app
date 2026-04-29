import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Configuration de la page (Design épuré)
st.set_page_config(
    page_title="VaxData | Collecte & Analyse",
    page_icon="​",
    layout="wide"
)

# 2. Barre latérale pour la navigation
with st.sidebar:
    st.title("VaxData 1.0")
    page = st.radio(
        "Menu Principal",
        ["Accueil", "Collecte de Données", "📊 Dashboard d'Analyse"],
        index=0
    )
    st.divider()
    st.info("Projet Universitaire - Collecte Vaccination (0-10 ans)")

# 3. Logique de la Page d'Accueil
if page == "Accueil":
    st.title("Bienvenue sur la plateforme VaxData")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### Mission de l'application
        Cette interface professionnelle est conçue pour les agents de santé et les administrateurs. 
        Elle permet de :
        * **Collecter** les données de vaccination en temps réel.
        * **Suivre** la couverture vaccinale par ville et par région.
        * **Analyser** les performances des campagnes mobiles par rapport aux hôpitaux.
        
        *Utilisez la barre latérale à gauche pour naviguer entre le formulaire de saisie et les analyses.*
        """)
    with col2:
        # Un visuel propre pour l'accueil
        st.image("https://images.unsplash.com/photo-1576091160550-2173dbc999ef?q=80&w=400", caption="Santé Publique")

# 4. Logique de Collecte (Avec Ville, Région et Contexte)
elif page == "Collecte de Données":
    st.header("Formulaire de Saisie")
    
    with st.form("vaccination_form", clear_on_submit=True):
        st.subheader("🔹 Identification de l'enfant")
        c1, c2 = st.columns(2)
        with c1:
            nom = st.text_input("Nom complet")
            age = st.slider("Âge (ans)", 0, 10, 5)
        with c2:
            vaccin = st.selectbox("Type de vaccin", ["BCG", "Polio", "DTC", "Rougeole", "Hépatite B", "Fièvre Jaune"])
            date_acte = st.date_input("Date d'administration")

        st.subheader("🔹 Localisation & Contexte")
        c3, c4 = st.columns(2)
        with c3:
            region = st.selectbox("Région", ["Centre", "Littoral", "Nord", "Ouest", "Est", "Sud", "Adamaoua", "Extrême-Nord", "Nord-Ouest", "Sud-Ouest"])
            ville = st.text_input("Ville / District")
        with c4:
            contexte = st.radio("Type de lieu", ["Hôpital / Centre de Santé", "Campagne de vaccination mobile"])

        submitted = st.form_submit_button("Enregistrer l'acte")
        
        if submitted:
            if nom and ville:
                # Création d'un dictionnaire pour les données
                nouvelle_donnee = {
                    "Nom": nom, "Age": age, "Vaccin": vaccin, 
                    "Date": str(date_acte), "Region": region, 
                    "Ville": ville, "Lieu": contexte
                }
                # Sauvegarde locale (CSV)
                df = pd.DataFrame([nouvelle_donnee])
                df.to_csv('data.csv', mode='a', index=False, header=not os.path.exists('data.csv'))
                st.success(f"Enregistrement validé pour {nom} ({ville})")
            else:
                st.error("Veuillez remplir le nom et la ville.")

# 5. Dashboard d'Analyse (Graphes et Statistiques)
elif page == "📊 Dashboard d'Analyse":
    st.header("📊 Analyse Descriptive des Données")

    if os.path.exists('data.csv'):
        df_load = pd.read_csv('data.csv')
        
        # --- Ligne 1 : Indicateurs Clés ---
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Total Vaccinés", len(df_load))
        kpi2.metric("Régions couvertes", df_load['Region'].nunique())
        kpi3.metric("Moyenne d'âge", round(df_load['Age'].mean(), 1))

        st.divider()

        # --- Ligne 2 : Graphiques ---
        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader("📍 Répartition par Région")
            fig_region = px.bar(df_load['Region'].value_counts(), 
                                color_discrete_sequence=['#2E7D32'],
                                labels={'value':'Nombre', 'index':'Région'})
            st.plotly_chart(fig_region, use_container_width=True)

        with col_right:
            st.subheader("Type de lieu d'administration")
            fig_lieu = px.pie(df_load, names='Lieu', 
                              color_discrete_sequence=['#004d99', '#808080'],
                              hole=0.4)
            st.plotly_chart(fig_lieu, use_container_width=True)

        # --- Ligne 3 : Histogramme de l'âge ---
        st.subheader("Distribution des âges des enfants")
        fig_age = px.histogram(df_load, x="Age", nbins=10, 
                               color_discrete_sequence=['#004d99'],
                               labels={'Age':'Âge de l\'enfant'})
        st.plotly_chart(fig_age, use_container_width=True)
        
        # Affichage du tableau brut
        with st.expander("Voir les données brutes"):
            st.dataframe(df_load, use_container_width=True)
    else:
        st.warning("Aucune donnée disponible. Veuillez d'abord remplir le formulaire.")
