import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestion Scolaire", page_icon="📚", layout="wide")

# Initialisation de la mémoire (Session State)
if "eleves" not in st.session_state:
    st.session_state.eleves = []

if "matieres" not in st.session_state:
    st.session_state.matieres = [
        {"nom": "Mathématiques", "coefficient": 4},
        {"nom": "Français", "coefficient": 4},
        {"nom": "Histoire-Géo", "coefficient": 2}
    ]

if "notes" not in st.session_state:
    st.session_state.notes = {} # Format: { (nom_eleve, nom_matiere): {"note": 15.0, "appreciation": "Bien"} }

st.title("📚 Application de Gestion Scolaire et Bulletins")

# Menu de navigation
menu = st.sidebar.selectbox("Navigation", ["1. Gestion des Élèves", "2. Gestion des Matières", "3. Saisie des Notes", "4. Consultation des Bulletins"])

# ==========================================
# 1. GESTION DES ÉLÈVES
# ==========================================
if menu == "1. Gestion des Élèves":
    st.header("👥 Gestion des Élèves")
    
    nouveau_nom = st.text_input("Nom complet de l'élève")
    if st.button("Ajouter l'élève"):
        if nouveau_nom and nouveau_nom not in st.session_state.eleves:
            st.session_state.eleves.append(nouveau_nom)
            st.success(f"Élève {nouveau_nom} ajouté avec succès !")
        else:
            st.warning("Veuillez entrer un nom valide ou un élève qui n'existe pas déjà.")

    st.subheader("Liste des élèves inscrits")
    if st.session_state.eleves:
        for i, eleve in enumerate(st.session_state.eleves, 1):
            col1, col2 = st.columns([4, 1])
            col1.write(f"{i}. {eleve}")
            if col2.button("Supprimer", key=f"del_eleve_{i}"):
                st.session_state.eleves.remove(eleve)
                st.rerun()
    else:
        st.info("Aucun élève enregistré pour le moment.")

# ==========================================
# 2. GESTION DES MATIÈRES ET COEFFICIENTS
# ==========================================
elif menu == "2. Gestion des Matières":
    st.header("📖 Gestion des Matières & Coefficients")
    
    nom_mat = st.text_input("Nom de la matière")
    coef_mat = st.number_input("Coefficient", min_value=1, max_value=10, value=2)
    
    if st.button("Ajouter la matière"):
        if nom_mat:
            st.session_state.matieres.append({"nom": nom_mat, "coefficient": coef_mat})
            st.success(f"Matière {nom_mat} ajoutée !")
            st.rerun()

    st.subheader("Matières actuelles")
    for mat in st.session_state.matieres:
        st.write(f"- **{mat['nom']}** (Coefficient : {mat['coefficient']})")

# ==========================================
# 3. SAISIE DES NOTES ET APPRÉCIATIONS
# ==========================================
elif menu == "3. Saisie des Notes":
    st.header("✍️ Saisie des Notes et Appréciations")

    if not st.session_state.eleves or not st.session_state.matieres:
        st.warning("Veuillez d'abord ajouter au moins un élève et une matière.")
    else:
        eleve_choisi = st.selectbox("Sélectionner un élève", st.session_state.eleves)
        
        st.subheader(notes_titre := f"Notes pour : {eleve_choisi}")
        
        for mat in st.session_state.matieres:
            nom_m = mat['nom']
            cle = (eleve_choisi, nom_m)
            
            note_actuelle = st.session_state.notes.get(cle, {}).get("note", 0.0)
            app_actuelle = st.session_state.notes.get(cle, {}).get("appreciation", "")
            
            col1, col2, col3 = st.columns([2, 2, 3])
            col1.markdown(f"**{nom_m}** (Coeff: {mat['coefficient']})")
            
            saisie_note = col2.number_input(f"Note /20", min_value=0.0, max_value=20.0, value=float(note_actuelle), key=f"note_{eleve_choisi}_{nom_m}")
            saisie_app = col3.text_input(f"Appréciation", value=app_actuelle, key=f"app_{eleve_choisi}_{nom_m}")
            
            st.session_state.notes[cle] = {
                "note": saisie_note,
                "appreciation": saisie_app
            }
        
        st.success("Les modifications sont enregistrées automatiquement au fur et à mesure.")

# ==========================================
# 4. CONSULTATION DES BULLETINS (AVEC RANG ET MOYENNE)
# ==========================================
elif menu == "4. Consultation les Bulletins":
    st.header("📊 Bulletins Scolaires, Moyennes et Classement")

    if not st.session_state.eleves:
        st.warning("Aucun élève enregistré.")
    else:
        # Étape 1 : Calculer les moyennes de tous les élèves pour établir le classement général
        classement_data = []
        
        for eleve in st.session_state.eleves:
            total_points = 0.0
            total_coeffs = 0
            
            for mat in st.session_state.matieres:
                nom_m = mat['nom']
                coeff = mat['coefficient']
                cle = (eleve, nom_m)
                
                note_info = st.session_state.notes.get(cle, {"note": 0.0})
                note = note_info.get("note", 0.0)
                
                total_points += note * coeff
                total_coeffs += coeff
            
            moyenne = total_points / total_coeffs if total_coeffs > 0 else 0.0
            classement_data.append({"eleve": eleve, "moyenne": moyenne, "total": total_points})
        
        # Trier les élèves par moyenne décroissante pour attribuer le rang
        classement_data = sorted(classement_data, key=lambda x: x["moyenne"], reverse=True)
        
        # Assigner les rangs (gérer l'affichage propre)
        for index, item in enumerate(classement_data):
            item["rang"] = index + 1

        # Étape 2 : Sélectionner l'élève à afficher
        noms_eleves = [item["eleve"] for item in classement_data]
        eleve_affiche = st.selectbox("Choisir l'élève dont vous voulez voir le bulletin", noms_eleves)
        
        # Retrouver les infos de l'élève sélectionné
        info_eleve = next(item for item in classement_data if item["eleve"] == eleve_affiche)
        
        st.markdown = f"### Bulletin de : {eleve_affiche}"
        st.info(f"🏆 **Rang dans la classe :** {info_eleve['rang']} / {len(st.session_state.eleves)}   |   ⭐ **Moyenne Générale :** {info_eleve['moyenne']:.2f} / 20   |   📌 **Total des points :** {info_eleve['total']:.2f}")

        # Tableau détaillé des notes
        tableau_notes = []
        for mat in st.session_state.matieres:
            nom_m = mat['nom']
            coeff = mat['coefficient']
            cle = (eleve_affiche, nom_m)
            
            note_info = st.session_state.notes.get(cle, {"note": 0.0, "appreciation": ""})
            note = note_info.get("note", 0.0)
            app = note_info.get("appreciation", "")
            
            total_matiere = note * coeff
            
            tableau_notes.append({
                "Matière": nom_m,
                "Coefficient": coeff,
                "Note /20": note,
                "Total (Note x Coeff)": total_matiere,
                "Appréciation du Professeur": app
            })
        
        df_notes = pd.DataFrame(tableau_notes)
        st.table(df_notes)