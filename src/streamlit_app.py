import streamlit as st
import requests
import pandas as pd
from datetime import datetime # Import nécessaire

# --- URLs API ---
API_BASE = "http://localhost:9876"
API_ME = f"{API_BASE}/me"
API_GPX = f"{API_BASE}/upload-gpx"
API_ACTIVITES = f"{API_BASE}/activites"
API_DELETE_ACTIVITE = f"{API_BASE}/activites" 
API_COMMENTAIRES = f"{API_BASE}/commentaires"
API_COMMENTAIRES_ACTIVITE = f"{API_BASE}/activites" # Gardé pour la compatibilité, mais le nouveau est meilleur

# --- AJOUTER CES LIGNES ---
API_UTILISATEUR_PSEUDO = f"{API_BASE}/utilisateurs/pseudo"
API_ABONNEMENTS = f"{API_BASE}/abonnements"
API_ABONNEMENTS_SUIVIS = f"{API_BASE}/abonnements/suivis"
API_JAIMES = f"{API_BASE}/jaimes"
# Note: Les URL pour GET /commentaires et /jaimes par activité seront construites dynamiquement

# --- Initialisation de la Session ---
if "connected" not in st.session_state:
    st.session_state["connected"] = False
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "username" not in st.session_state:
    st.session_state["username"] = None
if "password" not in st.session_state:
    st.session_state["password"] = None

st.title("Webservice Sports ENSAI") 

# --- 1. Formulaire d'authentification (Inchangé) ---
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


# --- 2. Analyse et Création d'activité (Inchangé) ---
def gpx_analyse_et_creation():
    """
    Gère l'upload, l'analyse (via /upload-gpx) et la création 
    (via /activites) d'un nouveau fichier GPX.
    """
    st.success(f"Connecté en tant que **{st.session_state['username']}** (ID: {st.session_state['user_id']})")
    st.subheader(" Importer une nouvelle activité (GPX)") 

    uploaded_file = st.file_uploader("Choisir un fichier GPX", type=["gpx"])

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
                st.subheader("Résumé de l'analyse")
                st.write(f"**Nom :** {activite.get('nom', '[inconnu]')}")
                st.write(f"**Type (issu du GPX) :** {activite.get('type', '[inconnu]')}") 
                st.write(f"**Distance (km) :** {activite.get('distance totale', '[inconnu]')}")
                st.write(f"**Durée (min) :** {activite.get('durée totale', '[inconnu]')}")
                st.write(f"**Vitesse moyenne (km/h) :** {activite.get('vitesse moyenne', '[inconnu]')}")

                st.session_state['analyse_data'] = activite
                st.session_state['uploaded_file_bytes'] = uploaded_file.getvalue()
                st.session_state['uploaded_file_name'] = uploaded_file.name

            except Exception as e:
                st.error(f"Erreur lors de l'analyse : {e}")
                if 'analyse_data' in st.session_state:
                    del st.session_state['analyse_data'] 

    if 'analyse_data' in st.session_state:
        st.write("---")
        st.markdown("#### Analyse réussie. Veuillez confirmer le sport avant de poster :") 
        
        sport = st.selectbox("Type de sport", ["course", "vélo", "randonnée", "marche"])
        
        if st.button("Poster cette activité"):
            try:
                st.session_state['sport_type'] = sport 

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

# --- 3. [MODIFIÉ] Affichage des activités (Générique) ---
def display_activity_list(activites_list: list, show_delete_button: bool = False):
    """
    Fonction générique pour afficher une liste d'activités,
    avec options pour liker, commenter, et supprimer.
    """
    if not activites_list:
        st.info("Aucune activité à afficher.")
        return

    auth = (st.session_state["username"], st.session_state["password"])
    logged_in_user_id = st.session_state["user_id"]

    for activite in activites_list:
        activity_id = activite.get('id_activite', 'N/A')
        activity_sport = activite.get('sport', 'N/A')
        activity_distance = activite.get('distance', 'N/A')
        activity_duree = activite.get('duree', 'N/A')
        
        if activity_duree is not None and activity_duree > 0:
            activity_vitesse = activity_distance / (activity_duree / 60)
            activity_vitesse_str = f"{activity_vitesse:.2f} km/h"
        else:
            activity_vitesse_str = "N/A"

        
        with st.expander(f"**Activité #{activity_id}** - {activity_sport} ({activity_distance} km)"):
            st.write(f"**Sport :** {activity_sport}")
            st.write(f"**Distance :** {activity_distance} km")
            st.write(f"**Durée :** {activity_duree} min")
            st.write(f"**Vitesse moyenne :** {activity_vitesse_str}")
            
            # --- BLOC LIKE ---
            try:
                # 1. Récupérer les likes pour cette activité
                resp_likes = requests.get(f"{API_ACTIVITES}/{activity_id}/jaimes", auth=auth)
                if resp_likes.status_code == 200:
                    likes_list = resp_likes.json()
                    like_count = len(likes_list)
                    # Vérifier si l'utilisateur connecté a déjà liké
                    user_has_liked = any(like['id_auteur'] == logged_in_user_id for like in likes_list)
                else:
                    like_count = 0
                    user_has_liked = False

                # 2. Afficher le bouton (Like ou Unlike)
                like_key = f"like_btn_{activity_id}"
                if user_has_liked:
                    if st.button(f"❤️ J'aime ({like_count})", key=like_key, help="Cliquer pour ne plus aimer"):
                        # Logique de "Unlike" (DELETE)
                        # NOTE : L'endpoint /jaimes/{id_activite}/{id_utilisateur} de doc/endpoints.md est utilisé
                        requests.delete(f"{API_JAIMES}/{activity_id}/{logged_in_user_id}", auth=auth)
                        st.rerun()
                else:
                    if st.button(f"🤍 J'aime ({like_count})", key=like_key, help="Cliquer pour aimer"):
                        # Logique de "Like" (POST)
                        # NOTE : L'endpoint /jaimes de doc/endpoints.md est utilisé
                        requests.post(API_JAIMES, params={"id_activite": activity_id}, auth=auth)
                        st.rerun()

            except Exception as e_like:
                st.error(f"Erreur 'Jaime': {e_like}")
            
            st.write("---")

            # --- BLOC COMMENTAIRES ---
            try:
                # 1. Afficher les commentaires existants
                st.markdown("**Commentaires :**")
                resp_comments = requests.get(f"{API_ACTIVITES}/{activity_id}/commentaires", auth=auth)
                if resp_comments.status_code == 200:
                    comments_list = resp_comments.json()
                    if not comments_list:
                        st.caption("Aucun commentaire pour l'instant.")
                    for comment in comments_list:
                        # (On suppose que le /commentaires renvoie aussi l'auteur, sinon il faut un autre appel)
                        # Pour l'instant, on affiche l'ID de l'auteur
                        auteur_id = comment.get('id_auteur', 'Inconnu')
                        texte = comment.get('commentaire', '')
                        date_com = comment.get('date_commentaire', '')
                        st.caption(f"Le {date_com}, {auteur_id} a dit :")
                        st.markdown(f"> {texte}")
                else:
                    st.error("Impossible de charger les commentaires.")
            
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
                                auth=auth
                            )
                            
                            if resp_comment.status_code == 200:
                                st.success("Commentaire ajouté !")
                                st.rerun()
                            else:
                                st.error(f"Erreur commentaire: {resp_comment.text}")
                        except Exception as e_comment:
                            st.error(f"Erreur: {e_comment}")

            except Exception as e_com_display:
                st.error(f"Erreur Commentaires: {e_com_display}")

            # --- BLOC SUPPRESSION (Conditionnel) ---
            if show_delete_button:
                st.divider()
                st.markdown("**Supprimer l'activité**")
                delete_key = f"delete_btn_{activity_id}"
                
                if st.button("Supprimer cette activité", key=delete_key, type="primary"):
                    try:
                        resp_delete = requests.delete(f"{API_DELETE_ACTIVITE}/{activity_id}", auth=auth)
                        resp_delete.raise_for_status() 
                        
                        st.success("Activité supprimée avec succès !")
                        if 'activites_list' in st.session_state:
                            del st.session_state['activites_list']
                        st.rerun()
                            
                    except Exception as e_delete:
                        st.error(f"Erreur de suppression : {e_delete.response.text if e_delete.response else e_delete}")


# --- 4. [MIS À JOUR] Section "Mes Activités" ---
def afficher_activites_personnelles():
    """
    Récupère et affiche la liste des activités de l'utilisateur connecté.
    Utilise maintenant la fonction générique display_activity_list.
    """
    st.subheader("Mes activités")
    
    if st.button("Afficher / Actualiser mes activités"):
        user_id = st.session_state["user_id"] 
        auth = (st.session_state["username"], st.session_state["password"])
        
        try:
            resp = requests.get(f"{API_ACTIVITES}/{user_id}", auth=auth)
            resp.raise_for_status() 
            st.session_state['activites_list'] = resp.json()
        except Exception as e:
            st.error(f"Erreur de requête : {e}")
            if 'activites_list' in st.session_state:
                del st.session_state['activites_list']

    if 'activites_list' in st.session_state:
        # APPEL DE LA NOUVELLE FONCTION
        display_activity_list(st.session_state['activites_list'], show_delete_button=True)

# --- 5. [NOUVEAU] Section "Rechercher un profil" ---
def afficher_recherche_profil():
    """
    Affiche un champ de recherche pour trouver un utilisateur par pseudo
    et afficher son profil (infos, bouton Suivre, activités).
    """
    st.subheader("Rechercher un Utilisateur")
    pseudo_recherche = st.text_input("Entrer le pseudo de l'utilisateur")
    
    if st.button("Rechercher"):
        st.session_state['profil_recherche'] = pseudo_recherche
        # Vider les anciens résultats lors d'une nouvelle recherche
        if 'profil_data' in st.session_state:
            del st.session_state['profil_data']
        if 'profil_activites' in st.session_state:
            del st.session_state['profil_activites']
        if 'profil_suivi' in st.session_state:
            del st.session_state['profil_suivi']

    if 'profil_recherche' in st.session_state:
        pseudo = st.session_state['profil_recherche']
        if not pseudo:
            return

        auth = (st.session_state["username"], st.session_state["password"])
        logged_in_user_id = st.session_state["user_id"]
        
        try:
            # 1. Récupérer les infos du profil
            if 'profil_data' not in st.session_state:
                resp_profil = requests.get(f"{API_UTILISATEUR_PSEUDO}/{pseudo}", auth=auth)
                if resp_profil.status_code == 404:
                    st.error(f"Utilisateur '{pseudo}' non trouvé.")
                    return
                resp_profil.raise_for_status()
                st.session_state['profil_data'] = resp_profil.json()

            profil_data = st.session_state['profil_data']
            profil_user_id = profil_data['id_utilisateur']

            # 2. Afficher les infos et le bouton "Suivre"
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"#### Profil de **{profil_data['pseudo']}**")
                st.caption(f"Nom : {profil_data.get('nom', 'N/A')} {profil_data.get('prenom', 'N/A')}")
            
            with col2:
                # Vérifier si on suit déjà cet utilisateur
                if 'profil_suivi' not in st.session_state:
                    resp_suivis = requests.get(f"{API_ABONNEMENTS_SUIVIS}/{logged_in_user_id}", auth=auth)
                    resp_suivis.raise_for_status()
                    liste_suivis = resp_suivis.json().get('suivis', [])
                    st.session_state['profil_suivi'] = profil_user_id in liste_suivis
                
                is_following = st.session_state['profil_suivi']

                # Ne pas afficher le bouton si on visite notre propre profil
                if profil_user_id != logged_in_user_id:
                    if is_following:
                        if st.button("Se désabonner", key=f"follow_btn_{profil_user_id}"):
                            requests.delete(API_ABONNEMENTS, params={"id_utilisateur_suiveur": logged_in_user_id, "id_utilisateur_suivi": profil_user_id}, auth=auth)
                            del st.session_state['profil_suivi'] # Forcer la re-vérification
                            st.rerun()
                    else:
                        if st.button("Suivre", key=f"follow_btn_{profil_user_id}", type="primary"):
                            requests.post(API_ABONNEMENTS, params={"id_utilisateur_suiveur": logged_in_user_id, "id_utilisateur_suivi": profil_user_id}, auth=auth)
                            del st.session_state['profil_suivi'] # Forcer la re-vérification
                            st.rerun()
            
            st.divider()
            
            # 3. Récupérer et afficher les activités du profil
            st.markdown(f"**Activités de {profil_data['pseudo']}**")
            if 'profil_activites' not in st.session_state:
                resp_activites = requests.get(f"{API_ACTIVITES}/{profil_user_id}", auth=auth)
                resp_activites.raise_for_status()
                st.session_state['profil_activites'] = resp_activites.json()

            # APPEL DE LA FONCTION GÉNÉRIQUE (sans le bouton supprimer)
            display_activity_list(st.session_state['profil_activites'], show_delete_button=False)

        except Exception as e:
            st.error(f"Erreur lors de la récupération du profil : {e}")
            if 'profil_data' in st.session_state:
                del st.session_state['profil_data']


# --- 6. [NOUVEAU] Section "Statistiques" (votre code) ---
def afficher_statistiques_personnelles():
    """
    Récupère et affiche les statistiques totales et hebdomadaires 
    de l'utilisateur connecté.
    """
    st.subheader("Mes Statistiques Personnelles")
    
    user_id = st.session_state["user_id"]
    auth = (st.session_state["username"], st.session_state["password"])

    # --- Statistiques Totales ---
    st.markdown("##### 📈 Statistiques Globales (agrégées par sport)")
    
    # Utilisation de st.cache_data ou st.session_state pour éviter les appels répétés
    if st.button("Afficher mes statistiques totales"):
        try:
            resp_total = requests.get(f"{API_STATS_TOTAL}/{user_id}", auth=auth)
            resp_total.raise_for_status()
            st.session_state['total_stats'] = resp_total.json() 
        except Exception as e:
            st.error(f"Erreur lors de la récupération des stats totales : {e}")
            if 'total_stats' in st.session_state:
                del st.session_state['total_stats']

    # Affichage si les stats totales sont chargées
    if 'total_stats' in st.session_state:
        stats_total = st.session_state['total_stats']
        
        # Récupérer les dictionnaires
        stats_nombre = stats_total.get('nombre_activites', {})
        stats_distance = stats_total.get('distance_totale', {})
        stats_duree_sec = stats_total.get('duree_totale_secondes', {})
        
        # Convertir les durées de secondes en minutes pour le graphique
        stats_duree_min = {sport: (secondes / 60) for sport, secondes in stats_duree_sec.items()}

        if not stats_nombre:
            st.info("Aucune activité totale à afficher.")
        else:
            # Graphique 1 : Nombre d'activités
            st.markdown("**Nombre d'activités par sport**")
            st.bar_chart(stats_nombre) 

            # Graphique 2 : Distance
            st.markdown("**Distance totale (km) par sport**")
            st.bar_chart(stats_distance)

            # Graphique 3 : Durée
            st.markdown("**Durée totale (minutes) par sport**")
            st.bar_chart(stats_duree_min)

    st.divider()

    # --- Statistiques Hebdomadaires ---
    st.markdown("##### 📅 Statistiques Hebdomadaires")
    
    date_ref = st.date_input("Choisir une date de référence pour la semaine")
    
    if st.button("Afficher les statistiques de la semaine"):
        date_str = date_ref.strftime("%Y-%m-%d")
        try:
            params = {"date_reference": date_str}
            resp_semaine = requests.get(f"{API_STATS_SEMAINE}/{user_id}", params=params, auth=auth)
            resp_semaine.raise_for_status()
            st.session_state['weekly_stats'] = resp_semaine.json()
            st.session_state['weekly_stats_date'] = date_str 
            
        except Exception as e:
            st.error(f"Erreur lors de la récupération des stats de la semaine : {e}")
            if 'weekly_stats' in st.session_state:
                del st.session_state['weekly_stats']

    if 'weekly_stats' in st.session_state:
        stats_semaine = st.session_state['weekly_stats']
        
        st.info(f"Affichage des statistiques pour la semaine du {st.session_state['weekly_stats_date']}")
        
        duree_min_semaine = stats_semaine.get('duree_semaine', 0) / 60
        
        col3, col4 = st.columns(2)
        col3.metric("Distance (Semaine)", f"{stats_semaine.get('distance_semaine', 0):.2f} km")
        col4.metric("Durée (Semaine)", f"{duree_min_semaine:.1f} minutes")
        
        stats_par_sport_semaine = stats_semaine.get('nombre_activites_semaine', {})
        if stats_par_sport_semaine:
            st.markdown("**Nombre d'activités (semaine)**")
            st.bar_chart(stats_par_sport_semaine)
        else:
            st.info("Aucune activité cette semaine-là.")


# --- Logique d'affichage principale ---
if not st.session_state["connected"]:
    auth_form()
else:
    # On utilise des onglets pour mieux organiser l'interface
    tab1, tab2, tab3, tab4 = st.tabs(["Poster Activité", "Mes Activités", "Mes Statistiques", "Rechercher Profil"])

    with tab1:
        gpx_analyse_et_creation()
    
    with tab2:
        afficher_activites_personnelles()
    
    with tab3:
        afficher_statistiques_personnelles()
        
    with tab4:
        afficher_recherche_profil()