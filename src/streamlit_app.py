import streamlit as st
import requests
import pandas as pd

# --- URLs API ---
API_BASE = "http://localhost:9876"
API_ME = f"{API_BASE}/me"
API_GPX = f"{API_BASE}/upload-gpx"
API_ACTIVITES = f"{API_BASE}/activites"
API_DELETE_ACTIVITE = f"{API_BASE}/activites" 
API_COMMENTAIRES = f"{API_BASE}/commentaires"
API_COMMENTAIRES_ACTIVITE = f"{API_BASE}/activites"

# --- Initialisation de la Session ---
if "connected" not in st.session_state:
    st.session_state["connected"] = False

st.title("Webservice Sports ENSAI") 

# --- 1. Formulaire d'authentification ---
def auth_form():
    """
    Affiche le formulaire de connexion.
    Récupère l'ID utilisateur numérique directement depuis /me lors de la connexion.
    """
    st.subheader("Connexion") 
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"): 
        try:
            resp_auth = requests.get(API_ME, auth=(username, password))
            
            if resp_auth.status_code == 200:
                st.session_state["username"] = username
                st.session_state["password"] = password
                
                donnees_auth = resp_auth.json()
                user_id = donnees_auth.get("id_utilisateur")

                if user_id is None:
                    st.error("Erreur : L'API /me n'a pas retourné d'ID utilisateur.")
                    st.session_state["connected"] = False
                else:
                    st.session_state["user_id"] = user_id
                    st.session_state["connected"] = True
                    st.success("Connecté avec succès !")
                    st.rerun()

            else:
                st.error("Identifiants incorrects.")
        
        except Exception as e_auth:
            st.error(f"Erreur de connexion : {e_auth}")


# --- 2. Analyse et Création d'activité ---
def gpx_analyse_et_creation():
    """
    Gère l'upload, l'analyse (via /upload-gpx) et la création 
    (via /activites) d'un nouveau fichier GPX.
    """
    st.success(f"Connecté en tant que **{st.session_state['username']}** (ID: {st.session_state['user_id']})")
    st.subheader(" Importer une nouvelle activité (GPX)") 

    uploaded_file = st.file_uploader("Choisir un fichier GPX", type=["gpx"])
    sport = st.selectbox("Type de sport", ["course", "vélo", "randonnée", "marche"])

    if uploaded_file is not None:
        if st.button("Analyser le fichier"):
            uploaded_file.seek(0) 
            files_analyse = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/gpx+xml")}
            
            try:
                with st.spinner("Analyse en cours..."):
                    resp = requests.post(API_GPX, files=files_analyse)
                    resp.raise_for_status()
                    data = resp.json()

                activite = data.get("activite", data)
                st.subheader("Résumé de l'analyse") # Titre corrigé
                st.write(f"**Nom :** {activite.get('nom', '[inconnu]')}")
                st.write(f"**Type :** {activite.get('type', sport)}")
                st.write(f"**Distance (km) :** {activite.get('distance totale', '[inconnu]')}")
                st.write(f"**Durée (min) :** {activite.get('durée totale', '[inconnu]')}")
                st.write(f"**Vitesse moyenne (km/h) :** {activite.get('vitesse moyenne', '[inconnu]')}")

                st.session_state['analyse_data'] = activite
                st.session_state['uploaded_file_bytes'] = uploaded_file.getvalue()
                st.session_state['uploaded_file_name'] = uploaded_file.name
                st.session_state['sport_type'] = sport

            except Exception as e:
                st.error(f"Erreur lors de l'analyse : {e}")
                if 'analyse_data' in st.session_state:
                    del st.session_state['analyse_data'] 

    if 'analyse_data' in st.session_state:
        st.write("---")
        st.markdown("#### Analyse réussie. Voulez-vous poster ") 
        
        if st.button("Poster cette activité"):
            try:
                files_create = {
                    "file": (
                        st.session_state['uploaded_file_name'], 
                        st.session_state['uploaded_file_bytes'], 
                        "application/gpx+xml"
                    )
                }
                
                resp_create = requests.post(
                    f"{API_ACTIVITES}",
                    files=files_create,
                    params={"sport": st.session_state['sport_type']},
                    auth=(st.session_state["username"], st.session_state["password"]),
                )
                
                if resp_create.status_code == 200:
                    st.success("Activité postée avec succès !") 
                    del st.session_state['analyse_data']
                    del st.session_state['uploaded_file_bytes']
                    del st.session_state['uploaded_file_name']
                    del st.session_state['sport_type']
                else:
                    st.error(f"Erreur de création : {resp_create.text}")
            except Exception as e:
                st.error(f"Erreur lors de la création : {e}")

# --- 3. Affichage des activités et ajout de commentaires ---
def afficher_activites_et_commenter():
    """
    Récupère et affiche la liste des activités de l'utilisateur.
    Permet d'ajouter un commentaire à n'importe quelle activité.
    """
    st.subheader("Mes activités")
    
    if st.button("Afficher / Actualiser mes activités"):
        
        user_id = st.session_state["user_id"] 
        auth = (st.session_state["username"], st.session_state["password"])
        
        try:
            resp = requests.get(f"{API_ACTIVITES}/{user_id}", auth=auth)
            resp.raise_for_status() 
            
            activites = resp.json()
            
            if not activites:
                st.info("Aucune activité trouvée.")
                st.session_state['activites_list'] = [] 
                return

            st.session_state['activites_list'] = activites 

        except Exception as e:
            st.error(f"Erreur de requête : {e}")
            if 'activites_list' in st.session_state:
                del st.session_state['activites_list']

    if 'activites_list' in st.session_state:
        activites = st.session_state['activites_list']
        
        if not activites:
            st.info("Aucune activité trouvée.")
            return
        
        auth = (st.session_state["username"], st.session_state["password"])

        for activite in activites:
            activity_id = activite.get('id_activite', 'N/A')
            activity_sport = activite.get('sport', 'N/A')
            activity_distance = activite.get('distance', 'N/A')
            activity_duree = activite.get('duree', 'N/A')
            
            if activity_duree is not None and activity_duree > 0:
                activity_vitesse = activity_distance / (activity_duree / 60)
                activity_vitesse_str = f"{activity_vitesse:.2f} km/h"
            else:
                activity_vitesse_str = "N/A"

            
            with st.expander(f"**{activity_id}** - {activity_sport}"):
                st.write(f"**Sport :** {activity_sport}")
                st.write(f"**Distance :** {activity_distance} km")
                st.write(f"**Durée :** {activity_duree} min")
                st.write(f"**Vitesse moyenne :** {activity_vitesse_str}")
                st.write(f"**ID de l'activité :** {activity_id}")
                
                st.write("---")
                st.markdown("**Ajouter un commentaire :**")

                comment_key = f"comment_text_{activity_id}"
                button_key = f"comment_btn_{activity_id}"
                
                commentaire_texte = st.text_area("Votre commentaire", key=comment_key, label_visibility="collapsed")
                
                if st.button("Envoyer", key=button_key):
                    if not commentaire_texte.strip():
                        st.warning("Le commentaire ne peut pas être vide.")
                    else:
                        try:
                            resp_comment = requests.post(
                                API_COMMENTAIRES,
                                params={
                                    "id_activite": activity_id,
                                    "commentaire": commentaire_texte
                                },
                                auth=(st.session_state["username"], st.session_state["password"])
                            )
                            
                            if resp_comment.status_code == 200:
                                st.success("Commentaire ajouté !")
                            else:
                                st.error(f"Erreur commentaire: {resp_comment.text}")
                        except Exception as e_comment:
                            st.error(f"Erreur: {e_comment}")

                st.divider()
                st.markdown("**Supprimer l'activité**")
                delete_key = f"delete_btn_{activity_id}"
                
                if st.button("Supprimer cette activité", key=delete_key):
                    try:
                        resp_delete = requests.delete(f"{API_DELETE_ACTIVITE}/{activity_id}", auth=auth)
                        resp_delete.raise_for_status() 
                        
                        st.success("Activité supprimée avec succès !")
                        
                        if 'activites_list' in st.session_state:
                            del st.session_state['activites_list']
                        st.rerun()
                            
                    except Exception as e_delete:
                        st.error(f"Erreur de suppression : {e_delete.response.text if e_delete.response else e_delete}")

if not st.session_state["connected"]:
    auth_form()
else:
    gpx_analyse_et_creation()
    st.divider()
    afficher_activites_et_commenter()