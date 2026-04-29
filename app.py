elif page == "Collecte de Données":
    st.header(" Enregistrement des données de vaccination")
    
    with st.form("vaccine_form", clear_on_submit=True):
        # Section 1 : Identification
        st.subheader(" Informations sur l'enfant")
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Nom complet de l'enfant")
            age = st.number_input("Âge (0-10 ans)", min_value=0, max_value=10)
        with col2:
            vaccin = st.selectbox("Type de vaccin", ["BCG", "Polio", "DTC", "Rougeole", "Hépatite B", "Fièvre Jaune"])
            date_vac = st.date_input("Date de l'acte")

        # Section 2 : Localisation (Ajout demandé)
        st.subheader("📍 Localisation")
        col3, col4 = st.columns(2)
        with col3:
            region = st.selectbox("Région", ["Centre", "Littoral", "Nord", "Extrême-Nord", "Ouest", "Sud", "Est", "Adamaoua", "Nord-Ouest", "Sud-Ouest"])
        with col4:
            ville = st.text_input("Ville / Localité")

        # Section 3 : Contexte (Ajout demandé)
        st.subheader("Contexte de l'administration")
        type_lieu = st.radio(
            "Où le vaccin a-t-il été administré ?",
            ["Hôpital / Centre de Santé", "Campagne de vaccination mobile"],
            horizontal=True
        )

        submit = st.form_submit_button("Valider l'enregistrement")
        
        if submit:
            if nom and ville:
                st.success(f"Enregistrement réussi pour {nom} à {ville} ({type_lieu})")
                # Ici vous ajouterez la logique pour sauvegarder dans un DataFrame ou une base de données
            else:
                st.error("Veuillez remplir tous les champs obligatoires (Nom et Ville).")