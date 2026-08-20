import pandas as pd
import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="EduGestion Pro - Gestion Scolaire",
    page_icon="🎓",
    layout="wide",
)

# Initialisation de la base de données en session
if "eleves" not in st.session_state:
    st.session_state.eleves = pd.DataFrame(
        columns=["Matricule", "Nom", "Prénom", "Classe"]
    )
if "matieres" not in st.session_state:
    st.session_state.matieres = pd.DataFrame(
        columns=["Code", "Matière", "Coefficient"]
    )
if "notes" not in st.session_state:
    st.session_state.notes = pd.DataFrame(
        columns=["Matricule", "Matière", "Note", "Trimestre"]
    )

# Barre latérale
st.sidebar.title("🎓 EduGestion Pro")
menu = st.sidebar.radio(
    "Navigation",
    [
        "📊 Tableau de Bord",
        "👨‍🎓 Élèves",
        "📚 Matières",
        "📝 Saisie & Calculs",
        "📄 Bulletins",
    ],
)

# ================= 1. TABLEAU DE BORD =================
if menu == "📊 Tableau de Bord":
    st.title("Tableau de Bord Administratif")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Élèves", len(st.session_state.eleves))
    with col2:
        st.metric("Total Matières", len(st.session_state.matieres))
    with col3:
        st.metric("Notes Enregistrées", len(st.session_state.notes))

# ================= 2. GESTION DES ÉLÈVES =================
elif menu == "👨‍🎓 Élèves":
    st.title("Gestion des Élèves")
    with st.form("form_eleve", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            matricule = st.text_input("Matricule")
            nom = st.text_input("Nom")
        with col2:
            prenom = st.text_input("Prénom")
            classe = st.selectbox(
                "Classe", ["6ème", "5ème", "4ème", "3ème", "2nde", "1ère", "Tle"]
            )
        if st.form_submit_button("Enregistrer"):
            if matricule and nom:
                new_row = pd.DataFrame(
                    [[matricule, nom, prenom, classe]],
                    columns=["Matricule", "Nom", "Prénom", "Classe"],
                )
                st.session_state.eleves = pd.concat(
                    [st.session_state.eleves, new_row], ignore_index=True
                )
                st.success("Élève ajouté avec succès !")

    if not st.session_state.eleves.empty:
        st.dataframe(st.session_state.eleves, use_container_width=True)

# ================= 3. GESTION DES MATIÈRES =================
elif menu == "📚 Matières":
    st.title("Gestion des Matières et Coefficients")
    with st.form("form_matiere", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            code = st.text_input("Code Matière")
        with col2:
            nom_mat = st.text_input("Nom de la Matière")
        with col3:
            coef = st.number_input("Coefficient", min_value=1, value=2)
        if st.form_submit_button("Ajouter Matière"):
            if code and nom_mat:
                new_mat = pd.DataFrame(
                    [[code, nom_mat, coef]], columns=["Code", "Matière", "Coefficient"]
                )
                st.session_state.matieres = pd.concat(
                    [st.session_state.matieres, new_mat], ignore_index=True
                )
                st.success("Matière ajoutée !")

    if not st.session_state.matieres.empty:
        st.dataframe(st.session_state.matieres, use_container_width=True)

# ================= 4. SAISIE & CALCULS (TOTAL, MOYENNE, RANG) =================
elif menu == "📝 Saisie & Calculs":
    st.title("Saisie des Notes & Calcul des Résultats")

    if st.session_state.eleves.empty or st.session_state.matieres.empty:
        st.warning("Veuillez d'abord ajouter des élèves et des matières.")
    else:
        trimestre = st.selectbox(
            "Sélectionner le Trimestre",
            ["Trimestre 1", "Trimestre 2", "Trimestre 3"],
        )
        matiere_saisie = st.selectbox(
            "Matière à évaluer", st.session_state.matieres["Matière"]
        )

        # Tableau de saisie rapide pour la matière sélectionnée
        st.subheader(f"Saisie des notes pour : {matiere_saisie}")
        df_saisie = st.session_state.eleves[["Matricule", "Nom", "Prénom"]].copy()

        # Récupérer les notes existantes si elles existent
        notes_existantes = st.session_state.notes[
            (st.session_state.notes["Matière"] == matiere_saisie)
            & (st.session_state.notes["Trimestre"] == trimestre)
        ]
        df_saisie = df_saisie.merge(
            notes_existantes[["Matricule", "Note"]], on="Matricule", how="left"
        )
        df_saisie["Note"] = df_saisie["Note"].fillna(0.0)

        edited_notes = st.data_editor(
            df_saisie,
            column_config={
                "Note": st.column_config.NumberColumn(
                    "Note (/20)", min_value=0.0, max_value=20.0, step=0.5
                )
            },
            use_container_width=True,
            key="editor_notes",
        )

        if st.button("Enregistrer les notes de cette matière"):
            # Mettre à jour les notes dans la session
            for index, row in edited_notes.iterrows():
                mat = row["Matricule"]
                note_val = row["Note"]
                # Supprimer l'ancienne note si elle existe
                st.session_state.notes = st.session_state.notes[
                    ~(
                        (st.session_state.notes["Matricule"] == mat)
                        & (st.session_state.notes["Matière"] == matiere_saisie)
                        & (st.session_state.notes["Trimestre"] == trimestre)
                    )
                ]
                # Ajouter la nouvelle
                new_n = pd.DataFrame(
                    [[mat, matiere_saisie, note_val, trimestre]],
                    columns=["Matricule", "Matière", "Note", "Trimestre"],
                )
                st.session_state.notes = pd.concat(
                    [st.session_state.notes, new_n], ignore_index=True
                )
            st.success("Notes enregistrées avec succès !")

        st.markdown("---")
        st.subheader("🏆 Classement, Totaux et Moyennes Générales")

        if not st.session_state.notes.empty:
            # Calcul automatique des totaux pondérés et moyennes
            resultats = []
            matieres_df = st.session_state.matieres
            total_coefficients = matieres_df["Coefficient"].sum()

            for idx, eleve in st.session_state.eleves.iterrows():
                mat = eleve["Matricule"]
                notes_eleve = st.session_state.notes[
                    (st.session_state.notes["Matricule"] == mat)
                    & (st.session_state.notes["Trimestre"] == trimestre)
                ]

                total_points = 0
                for _, n_row in notes_eleve.iterrows():
                    match_coef = matieres_df[
                        matieres_df["Matière"] == n_row["Matière"]
                    ]
                    if not match_coef.empty:
                        coef = match_coef.iloc[0]["Coefficient"]
                        total_points += n_row["Note"] * coef

                moyenne = (
                    total_points / total_coefficients
                    if total_coefficients > 0
                    else 0
                )
                resultats.append(
                    {
                        "Matricule": mat,
                        "Nom": eleve["Nom"],
                        "Prénom": eleve["Prénom"],
                        "Total Général": round(total_points, 2),
                        "Moyenne (/20)": round(moyenne, 2),
                    }
                )

            df_res = pd.DataFrame(resultats)
            if not df_res.empty:
                # Calcul du rang basé sur la moyenne
                df_res = df_res.sort_values(
                    by="Moyenne (/20)", ascending=False
                ).reset_index(drop=True)
                df_res["Rang"] = range(1, len(df_res) + 1)
                # Réorganiser les colonnes
                df_res = df_res[
                    [
                        "Rang",
                        "Matricule",
                        "Nom",
                        "Prénom",
                        "Total Général",
                        "Moyenne (/20)",
                    ]
                ]

                st.dataframe(df_res, use_container_width=True)

# ================= 5. BULLETINS =================
elif menu == "📄 Bulletins":
    st.title("Impression des Bulletins")
    st.info(
        "Module de génération de bulletins individuels basé sur les moyennes calculées."
    )