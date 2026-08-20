import pandas as pd
import streamlit as st

st.set_page_config(page_title="ProGestion Scolaire", layout="wide")

st.title("🎓 ProGestion Scolaire - Gestion Professionnelle")

# --- INITIALISATION DE LA MÉMOIRE ---
if "eleves" not in st.session_state:
  st.session_state["eleves"] = []

if "notes_df" not in st.session_state:
  # Tableau initial avec les matières et leurs coefficients par défaut
  st.session_state["notes_df"] = pd.DataFrame(
      columns=[
          "Élève",
          "Mathématiques (Coef 4)",
          "Français (Coef 4)",
          "Histoire-Géo (Coef 2)",
          "Sciences (Coef 3)",
          "Anglais (Coef 2)",
      ]
  )

# Menu de navigation latéral
menu = st.sidebar.radio(
    "Navigation",
    ["👥 Gestion des Élèves", "📝 Saisie des Notes en Tableau", "📄 Bulletins & Classement"],
)

# --- SECTION 1 : GESTION DES ÉLÈVES ---
if menu == "👥 Gestion des Élèves":
  st.header("👥 Inscription des Élèves")
  nom_eleve = st.text_input("Nom complet de l'élève")

  if st.button("Ajouter l'élève"):
    if nom_eleve.strip() != "":
      if nom_eleve not in st.session_state["eleves"]:
        st.session_state["eleves"].append(nom_eleve)

        # Ajouter automatiquement une ligne vide pour cet élève dans le tableau des notes
        nouvelle_ligne = {
            "Élève": nom_eleve,
            "Mathématiques (Coef 4)": 0.0,
            "Français (Coef 4)": 0.0,
            "Histoire-Géo (Coef 2)": 0.0,
            "Sciences (Coef 3)": 0.0,
            "Anglais (Coef 2)": 0.0,
        }
        st.session_state["notes_df"] = pd.concat(
            [
                st.session_state["notes_df"],
                pd.DataFrame([nouvelle_ligne]),
            ],
            ignore_index=True,
        )

        st.success(f"Élève {nom_eleve} ajouté avec succès !")
      else:
        st.warning("Cet élève est déjà enregistré.")
    else:
      st.error("Veuillez entrer un nom valide.")

  st.subheader(f"Effectif total de la classe : {len(st.session_state['eleves'])}")
  if st.session_state["eleves"]:
    for e in st.session_state["eleves"]:
      st.write(f"- {e}")
  else:
    st.info("Aucun élève enregistré pour le moment.")

# --- SECTION 2 : SAISIE DES NOTES EN TABLEAU ---
elif menu == "📝 Saisie des Notes en Tableau":
  st.header("📝 Grille de Saisie des Notes")

  if len(st.session_state["eleves"]) == 0:
    st.warning("Veuillez d'abord enregistrer des élèves dans l'onglet 1.")
  else:
    st.write(
        "Modifiez directement les notes dans le tableau ci-dessous (cliquez"
        " dans une case pour changer la note), puis cliquez sur le bouton"
        " d'enregistrement."
    )

    # Tableau interactif modifiable
    notes_modifiees = st.data_editor(
        st.session_state["notes_df"], num_rows="fixed", use_container_width=True
    )

    if st.button("💾 Enregistrer toutes les modifications"):
      st.session_state["notes_df"] = notes_modifiees
      st.success("Toutes les notes ont été enregistrées avec succès !")

# --- SECTION 3 : BULLETINS & CLASSEMENT ---
elif menu == "📄 Bulletins & Classement":
  st.header("📄 Édition des Bulletins Scolaires")

  if (
      len(st.session_state["eleves"]) == 0
      or st.session_state["notes_df"].empty
  ):
    st.warning("Veuillez ajouter des élèves et saisir des notes au préalable.")
  else:
    effectif_classe = len(st.session_state["eleves"])
    coefficients = {
        "Mathématiques (Coef 4)": 4,
        "Français (Coef 4)": 4,
        "Histoire-Géo (Coef 2)": 2,
        "Sciences (Coef 3)": 3,
        "Anglais (Coef 2)": 2,
    }
    total_coefs = sum(coefficients.values())

    # --- CALCUL AUTOMATIQUE DES MOYENNES ET DES RANGS ---
    classement_data = []
    for index, row in st.session_state["notes_df"].iterrows():
      el = row["Élève"]
      total_points = sum(row[mat] * coefficients[mat] for mat in coefficients)
      moyenne_el = total_points / total_coefs
      classement_data.append({"Élève": el, "Moyenne": moyenne_el})

    df_classement = pd.DataFrame(classement_data)
    # Trier par moyenne décroissante pour attribuer le rang
    df_classement = df_classement.sort_values(
        by="Moyenne", ascending=False
    ).reset_index(drop=True)
    df_classement["Rang"] = df_classement.index + 1

    # --- CHOIX DE L'ÉLÈVE ---
    eleve_selectionne = st.selectbox(
        "Sélectionnez l'élève dont vous voulez afficher le bulletin",
        st.session_state["eleves"],
    )

    st.markdown("---")
    col1, col2 = st.columns(2)
    col1.write("**Établissement Scolaire**")
    col1.write(f"**Élève :** {eleve_selectionne}")
    col2.write(f"**Année Scolaire :** 2025-2026")
    col2.write(f"**Effectif de la classe :** {effectif_classe} élèves")

    # Récupérer la ligne de notes de l'élève
    ligne_eleve = st.session_state["notes_df"][
        st.session_state["notes_df"]["Élève"] == eleve_selectionne
    ]

    if not ligne_eleve.empty:
      r = ligne_eleve.iloc[0]
      details_bulletin = []
      total_pts_eleve = 0

      for mat, coef in coefficients.items():
        note_val = r[mat]
        total_mat = note_val * coef
        total_pts_eleve += total_mat
        details_bulletin.append({
            "Matière": mat.split(" (")[0],
            "Note /20": note_val,
            "Coefficient": coef,
            "Total Obtenu": total_mat,
        })

      df_bul = pd.DataFrame(details_bulletin)
      st.subheader("Tableau des Notes et Résultats")
      st.table(df_bul)

      moyenne_generale = total_pts_eleve / total_coefs
      rang_eleve = df_classement.loc[
          df_classement["Élève"] == eleve_selectionne, "Rang"
      ].values[0]

      st.markdown("---")
      c1, c2, c3 = st.columns(3)
      c1.metric(
          label="Total des Points",
          value=f"{total_pts_eleve} / {total_coefs * 20}",
      )
      c2.metric(label="Moyenne Générale", value=f"{moyenne_generale:.2f} / 20")
      c3.metric(
          label="Rang de l'élève", value=f"{rang_eleve} / {effectif_classe}"
      )

      # Appréciation automatique
      if moyenne_generale >= 16:
        appreciation = (
            "Excellent travail ! Tableau d'honneur et félicitations du conseil."
        )
      elif moyenne_generale >= 14:
        appreciation = "Très bon trimestre. Encouragements."
      elif moyenne_generale >= 12:
        appreciation = "Bon travail. Poursuivez ainsi."
      elif moyenne_generale >= 10:
        appreciation = "Travail passable. Des efforts attendus."
      else:
        appreciation = "Insuffisant. Redoublez d'efforts au prochain trimestre."

      st.info(f"**Appréciation générale :** {appreciation}")