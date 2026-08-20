import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Gestion Scolaire", page_icon="📚", layout="wide"
)

st.title("📚 Application de Gestion Scolaire et Bulletins")

# Menu de navigation
menu = st.sidebar.selectbox("Navigation", ["1. Gestion des Élèves", "2. Saisie des Notes"])

# Initialisation des listes dans la mémoire de l'application
if "eleves" not in st.session_state:
  st.session_state["eleves"] = []

if "notes_df" not in st.session_state:
  # DataFrame vide par défaut pour les notes
  st.session_state["notes_df"] = pd.DataFrame(
      columns=["Élève", "Mathématiques", "Français", "Histoire-Géo", "Sciences"]
  )

# --- SECTION 1 : GESTION DES ÉLÈVES ---
if menu == "1. Gestion des Élèves":
  st.header("👥 Gestion des Élèves")

  nom_eleve = st.text_input("Nom complet de l'élève")
  if st.button("Ajouter l'élève"):
    if nom_eleve.strip() != "":
      if nom_eleve not in st.session_state["eleves"]:
        st.session_state["eleves"].append(nom_eleve)

        # Mettre à jour le tableau des notes pour y ajouter ce nouvel élève
        nouvelle_ligne = pd.DataFrame(
            [[nom_eleve, 0.0, 0.0, 0.0, 0.0]], columns=st.session_state["notes_df"].columns
        )
        st.session_state["notes_df"] = pd.concat(
            [st.session_state["notes_df"], nouvelle_ligne], ignore_index=True
        )

        st.success(f"Élève {nom_eleve} ajouté avec succès !")
      else:
        st.warning("Cet élève existe déjà.")
    else:
      st.error("Veuillez entrer un nom valide.")

  st.subheader("Liste des élèves inscrits")
  if len(st.session_state["eleves"]) > 0:
    for e in st.session_state["eleves"]:
      st.write(f"- {e}")
  else:
    st.info("Aucun élève enregistré pour le moment.")

# --- SECTION 2 : SAISIE DES NOTES EN TABLEAU ---
elif menu == "2. Saisie des Notes":
  st.header("📝 Saisie des Notes par Matière")

  if len(st.session_state["eleves"]) == 0:
    st.warning("Veuillez d'abord enregistrer des élèves dans l'onglet 1.")
  else:
    st.write(
        "Modifiez directement les notes dans le tableau ci-dessous, puis"
        " cliquez sur Enregistrer."
    )

    # Utilisation de st.data_editor pour un tableau modifiable interactivement
    notes_modifiees = st.data_editor(
        st.session_state["notes_df"], num_rows="fixed", use_container_width=True
    )

    if st.button("Enregistrer toutes les notes"):
      st.session_state["notes_df"] = notes_modifiees
      st.success("Notes enregistrées avec succès !")

    st.subheader("Aperçu du tableau récapitulatif")
    st.table(st.session_state["notes_df"])