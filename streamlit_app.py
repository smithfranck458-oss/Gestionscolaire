import pandas as pd
import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="EduGestion - Système de Gestion Scolaire",
    page_icon="🎓",
    layout="wide",
)

# Style CSS personnalisé pour un design moderne et professionnel
st.markdown(
    """
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
    }
    </style>
""",
    unsafe_allow_html=True,
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

# Barre latérale de navigation moderne
st.sidebar.title("🎓 EduGestion Pro")
st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Navigation",
    [
        "📊 Tableau de Bord",
        "👨‍🎓 Gestion des Élèves",
        "📚 Gestion des Matières",
        "📝 Saisie des Notes",
        "📄 Bulletins & Rapports",
    ],
)

# ================= MODULE 1 : TABLEAU DE BORD =================
if menu == "📊 Tableau de Bord":
    st.title("Tableau de Bord Administratif")
    st.markdown("Vue d'ensemble de l'établissement scolaire.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"""<div class="metric-card"><h3>Total Élèves</h3><h2>{len(st.session_state.eleves)}</h2></div>""",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""<div class="metric-card"><h3>Total Matières</h3><h2>{len(st.session_state.matieres)}</h2></div>""",
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"""<div class="metric-card"><h3>Notes Enregistrées</h3><h2>{len(st.session_state.notes)}</h2></div>""",
            unsafe_allow_html=True,
        )

# ================= MODULE 2 : GESTION DES ÉLÈVES =================
elif menu == "👨‍🎓 Gestion des Élèves":
    st.title("Gestion des Élèves")

    with st.form("form_eleve", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            matricule = st.text_input("Numéro de Matricule")
            nom = st.text_input("Nom de l'élève")
        with col2:
            prenom = st.text_input("Prénom de l'élève")
            classe = st.selectbox(
                "Classe", ["6ème", "5ème", "4ème", "3ème", "2nde", "1ère", "Tle"]
            )

        submit = st.form_submit_button("Enregistrer l'élève")
        if submit and matricule and nom:
            new_row = pd.DataFrame(
                [[matricule, nom, prenom, classe]],
                columns=["Matricule", "Nom", "Prénom", "Classe"],
            )
            st.session_state.eleves = pd.concat(
                [st.session_state.eleves, new_row], ignore_index=True
            )
            st.success(
                f"L'élève {nom} {prenom} a été enregistré avec succès !"
            )

    st.subheader("Liste des Élèves Inscrits")
    if not st.session_state.eleves.empty:
        st.dataframe(st.session_state.eleves, use_container_width=True)
    else:
        st.info("Aucun élève enregistré pour le moment.")

# ================= MODULE 3 : GESTION DES MATIÈRES =================
elif menu == "📚 Gestion des Matières":
    st.title("Gestion des Matières et Coefficients")

    with st.form("form_matiere", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            code = st.text_input("Code Matière (ex: MATH)")
        with col2:
            nom_matiere = st.text_input("Nom de la Matière")
        with col3:
            coef = st.number_input("Coefficient", min_value=1, max_value=10, value=2)

        submit_mat = st.form_submit_button("Ajouter la Matière")
        if submit_mat and code and nom_matiere:
            new_mat = pd.DataFrame(
                [[code, nom_matiere, coef]], columns=["Code", "Matière", "Coefficient"]
            )
            st.session_state.matieres = pd.concat(
                [st.session_state.matieres, new_mat], ignore_index=True
            )
            st.success(f"Matière {nom_matiere} ajoutée !")

    st.subheader("Matières Disponibles")
    if not st.session_state.matieres.empty:
        st.dataframe(st.session_state.matieres, use_container_width=True)
    else:
        st.info("Aucune matière configurée.")

# ================= MODULE 4 : SAISIE DES NOTES =================
elif menu == "📝 Saisie des Notes":
    st.title("Saisie des Notes")

    if st.session_state.eleves.empty or st.session_state.matieres.empty:
        st.warning(
            "Veuillez d'abord enregistrer au moins un élève et une matière."
        )
    else:
        with st.form("form_note", clear_on_submit=True):
            eleve_choisi = st.selectbox(
                "Sélectionner l'élève",
                st.session_state.eleves["Matricule"]
                + " - "
                + st.session_state.eleves["Nom"],
            )
            matiere_choisie = st.selectbox(
                "Sélectionner la matière", st.session_state.matieres["Matière"]
            )
            trimestre = st.selectbox(
                "Période", ["Trimestre 1", "Trimestre 2", "Trimestre 3"]
            )
            note = st.number_input(
                "Note (/20)", min_value=0.0, max_value=20.0, step=0.5
            )

            submit_note = st.form_submit_button("Valider la note")
            if submit_note:
                mat_id = eleve_choisi.split(" - ")[0]
                new_n = pd.DataFrame(
                    [[mat_id, matiere_choisie, note, trimestre]],
                    columns=["Matricule", "Matière", "Note", "Trimestre"],
                )
                st.session_state.notes = pd.concat(
                    [st.session_state.notes, new_n], ignore_index=True
                )
                st.success("Note enregistrée avec succès !")

        st.subheader("Historique des Notes")
        if not st.session_state.notes.empty:
            st.dataframe(st.session_state.notes, use_container_width=True)

# ================= MODULE 5 : BULLETINS & RAPPORTS =================
elif menu == "📄 Bulletins & Rapports":
    st.title("Génération des Bulletins Scolaires")

    if st.session_state.eleves.empty or st.session_state.notes.empty:
        st.info("Données insuffisantes pour générer les bulletins.")
    else:
        selected_eleve = st.selectbox(
            "Choisir un élève pour voir son bulletin",
            st.session_state.eleves["Matricule"]
            + " - "
            + st.session_state.eleves["Nom"],
        )
        matricule_sel = selected_eleve.split(" - ")[0]
        trimestre_sel = st.selectbox(
            "Choisir le trimestre", ["Trimestre 1", "Trimestre 2", "Trimestre 3"]
        )

        if st.button("Générer le Bulletin"):
            st.markdown(f"---")
            st.markdown(f"### 🏫 BULLETIN SCOLAIRE - {trimestre_sel}")

            eleve_info = st.session_state.eleves[
                st.session_state.eleves["Matricule"] == matricule_sel
            ].iloc[0]
            st.markdown(
                f"**Élève :** {eleve_info['Nom']} {eleve_info['Prénom']} | **Matricule :** {eleve_info['Matricule']} | **Classe :** {eleve_info['Classe']}"
            )

            # Récupération des notes de l'élève
            notes_eleve = st.session_state.notes[
                (st.session_state.notes["Matricule"] == matricule_sel)
                & (st.session_state.notes["Trimestre"] == trimestre_sel)
            ]

            if not notes_eleve.empty:
                st.dataframe(notes_eleve, use_container_width=True)
                st.success("Bulletin généré avec succès. Prêt pour impression ou export PDF.")
            else:
                st.warning("Aucune note trouvée pour cet élève sur cette période.")