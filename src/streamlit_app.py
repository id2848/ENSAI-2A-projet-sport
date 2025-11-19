# streamlit_app.py
import streamlit as st
import requests
from datetime import datetime
from typing import Any

# --- URLs API ---
API_BASE = "http://localhost:9876"
API_ME = f"{API_BASE}/me"
API_GPX = f"{API_BASE}/upload-gpx"
API_ACTIVITES = f"{API_BASE}/activites"
API_ACTIVITE_BY_ID = f"{API_BASE}/activites"  # used as f"{API_ACTIVITE_BY_ID}/{id}"
API_DELETE_ACTIVITE = f"{API_BASE}/activites" 
API_COMMENTAIRES = f"{API_BASE}/commentaires"
API_UPLOAD_GPX = f"{API_BASE}/upload-gpx"
API_UTILISATEUR_PSEUDO = f"{API_BASE}/utilisateurs/pseudo"
API_ABONNEMENTS = f"{API_BASE}/abonnements"
API_ABONNEMENTS_SUIVIS = f"{API_BASE}/abonnements/suivis"
API_JAIMES = f"{API_BASE}/jaimes"
API_JAIMES_EXISTE = f"{API_BASE}/jaimes/existe"
API_STATS_TOTAL = f"{API_BASE}/statistiques/total"
API_STATS_SEMAINE = f"{API_BASE}/statistiques/semaine"
API_LOGOUT = f"{API_BASE}/logout"

# --- Session initialization ---
if "connected" not in st.session_state:
    st.session_state["connected"] = False
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "username" not in st.session_state:
    st.session_state["username"] = None
if "password" not in st.session_state:
    st.session_state["password"] = None

st.set_page_config(page_title="Webservice Sports ENSAI", layout="wide")
st.title("Webservice Sports ENSAI")

# --- Utility helpers ---
def auth_tuple() -> tuple[str, str] | None:
    if st.session_state.get("username") and st.session_state.get("password"):
        return (st.session_state["username"], st.session_state["password"])
    return None

def safe_json(resp: requests.Response) -> Any:
    try:
        return resp.json()
    except Exception:
        return resp.text

def extract_activity_field(a: dict, *keys, default=None):
    for k in keys:
        if k in a:
            return a[k]
    return default

def normalize_activity(activite_raw: dict) -> dict:
    """
    Normalize different possible keys to a standard structure used by the UI:
    - id_activite, sport, distance (km), duree (minutes), date, nom
    """
    a = {}
    a['id_activite'] = extract_activity_field(activite_raw, 'id_activite', 'id', 'id_activity', default=None)
    a['sport'] = extract_activity_field(activite_raw, 'sport', 'type', default='inconnu')
    # distance: try common keys; if distance given as meters convert to km if > 1000
    dist = extract_activity_field(activite_raw, 'distance', 'distance totale', 'distance_km', 'distance_m', default=None)
    if isinstance(dist, str):
        try:
            dist = float(dist.replace(',', '.'))
        except Exception:
            dist = None
    if isinstance(dist, (int, float)):
        # Heuristic: if distance > 1000 it's probably in meters
        if dist > 1000:
            dist = dist / 1000.0
    a['distance'] = dist if dist is not None else 0.0
    # duree: minutes or seconds?
    duree = extract_activity_field(activite_raw, 'duree', 'durée totale', 'duree_minutes', 'duree_secondes', default=None)
    if isinstance(duree, str):
        try:
            duree = float(duree.replace(',', '.'))
        except Exception:
            duree = None
    if isinstance(duree, (int, float)):
        # If very large, assume seconds -> convert to minutes
        if duree > 10000:
            duree = duree / 60.0
        elif duree > 300 and duree < 10000 and 'secondes' in str(list(activite_raw.keys())).lower():
            # ambiguous - but keep as minutes if reasonable
            pass
    a['duree'] = duree if duree is not None else 0.0
    a['date'] = extract_activity_field(activite_raw, 'date', 'date_activite', 'start_time', default=None)
    a['nom'] = extract_activity_field(activite_raw, 'nom', 'name', default='')
    return a

# --- 1. Auth form ---
def auth_form():
    st.subheader("Connexion")
    username = st.text_input("Nom d'utilisateur", value=st.session_state.get("username",""))
    password = st.text_input("Mot de passe", type="password", value=st.session_state.get("password",""))

    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("Se connecter"):
            try:
                resp = requests.get(API_ME, auth=(username, password))
                if resp.status_code == 200:
                    user = resp.json()
                    # user must contain id_utilisateur
                    uid = user.get("id_utilisateur") or user.get("id") or user.get("id_user")
                    if uid is None:
                        st.error("L'API /me n'a pas retourné d'ID utilisateur.")
                        return
                    st.session_state["username"] = username
                    st.session_state["password"] = password
                    st.session_state["user_id"] = uid
                    st.session_state["connected"] = True
                    st.success("Connecté avec succès !")
                    st.experimental_rerun()
                else:
                    st.error(f"Échec d'authentification : {resp.status_code} - {safe_json(resp)}")
            except Exception as e:
                st.error(f"Erreur de connexion : {e}")

    with col2:
        if st.button("Se déconnecter"):
            # clear session
            st.session_state["connected"] = False
            st.session_state["username"] = None
            st.session_state["password"] = None
            st.session_state["user_id"] = None
            st.success("Déconnecté")
            st.experimental_rerun()

# --- 2. GPX upload and create activity ---
def gpx_analyse_et_creation():
    st.subheader("Importer une nouvelle activité (GPX)")
    st.success(f"Connecté en tant que **{st.session_state['username']}** (ID: {st.session_state['user_id']})")

    uploaded_file = st.file_uploader("Choisir un fichier GPX", type=["gpx"])
    if uploaded_file is not None:
        if st.button("Analyser le fichier"):
            uploaded_file.seek(0)
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/gpx+xml")}
            try:
                resp = requests.post(API_UPLOAD_GPX, files=files)
                if resp.status_code == 200:
                    data = resp.json()
                    activite = data.get("activite", data)
                    st.session_state['analyse_data'] = activite
                    st.session_state['uploaded_file_bytes'] = uploaded_file.getvalue()
                    st.session_state['uploaded_file_name'] = uploaded_file.name
                    st.success("Analyse réussie.")
                else:
                    st.error(f"Erreur d'analyse : {resp.status_code} - {safe_json(resp)}")
            except Exception as e:
                st.error(f"Erreur lors de l'analyse : {e}")

    if 'analyse_data' in st.session_state:
        st.markdown("#### Résumé de l'analyse")
        activite = st.session_state['analyse_data']
        st.write(f"**Nom :** {activite.get('nom', activite.get('name','[inconnu]'))}")
        st.write(f"**Type (issu du GPX) :** {activite.get('type', '[inconnu]')}")
        st.write(f"**Distance (km) :** {activite.get('distance totale', activite.get('distance', '[inconnu]'))}")
        st.write(f"**Durée (min) :** {activite.get('durée totale', activite.get('duree', '[inconnu]'))}")
        st.write(f"**Vitesse moyenne (km/h) :** {activite.get('vitesse moyenne', '[inconnu]')}")
        st.write("---")
        sport = st.selectbox("Type de sport", ["course", "vélo", "randonnée", "marche"])
        if st.button("Poster cette activité"):
            files_create = {
                "file": (
                    st.session_state['uploaded_file_name'],
                    st.session_state['uploaded_file_bytes'],
                    "application/gpx+xml"
                )
            }
            try:
                resp = requests.post(
                    API_ACTIVITES,
                    files=files_create,
                    params={"sport": sport},
                    auth=(st.session_state["username"], st.session_state["password"])
                )
                if resp.status_code == 200:
                    st.success("Activité postée avec succès !")
                    # clear analysis state
                    for k in ['analyse_data','uploaded_file_bytes','uploaded_file_name']:
                        if k in st.session_state:
                            del st.session_state[k]
                    st.experimental_rerun()
                else:
                    st.error(f"Erreur lors de la création : {resp.status_code} - {safe_json(resp)}")
            except Exception as e:
                st.error(f"Erreur lors de la création : {e}")

# --- 3. Generic activity display (with likes/comments/delete) ---
def display_activity_list(activites_list: list[dict], show_delete_button: bool = False):
    if not activites_list:
        st.info("Aucune activité à afficher.")
        return

    auth = (st.session_state["username"], st.session_state["password"])
    logged_in_user_id = st.session_state["user_id"]

    for raw in activites_list:
        a = normalize_activity(raw)
        activity_id = a.get('id_activite') or a.get('id') or "[N/A]"
        activity_sport = a.get('sport', 'N/A')
        activity_distance = a.get('distance', 0.0)
        activity_duree = a.get('duree', 0.0)

        try:
            if activity_duree and float(activity_duree) > 0:
                activity_vitesse = float(activity_distance) / (float(activity_duree) / 60.0)
                activity_vitesse_str = f"{activity_vitesse:.2f} km/h"
            else:
                activity_vitesse_str = "N/A"
        except Exception:
            activity_vitesse_str = "N/A"

        expander_label = f"Activité #{activity_id} — {activity_sport} ({activity_distance} km)"
        with st.expander(expander_label):
            st.write(f"**Sport :** {activity_sport}")
            st.write(f"**Distance :** {activity_distance} km")
            st.write(f"**Durée :** {activity_duree} min")
            st.write(f"**Vitesse moyenne :** {activity_vitesse_str}")
            st.write(f"**Date :** {a.get('date','N/A')}")
            st.write("---")

            # --- LIKE / UNLIKE (using /jaimes/existe for current user) ---
            try:
                # Check if current user liked this activity
                params_exist = {"id_activite": activity_id, "id_auteur": logged_in_user_id}
                resp_exist = requests.get(API_JAIMES_EXISTE, params=params_exist, auth=auth)
                user_has_liked = False
                if resp_exist.status_code == 200:
                    # API returns a raw boolean true/false
                    try:
                        user_has_liked = bool(resp_exist.json())
                    except Exception:
                        # fallback: parse text
                        user_has_liked = str(resp_exist.text).lower() in ("true", "1")
                else:
                    # treat as not liked if error
                    user_has_liked = False

                like_key = f"like_btn_{activity_id}"
                if user_has_liked:
                    if st.button(f"💔 Retirer le J'aime", key=like_key):
                        try:
                            resp_del = requests.delete(f"{API_JAIMES}/{activity_id}/{logged_in_user_id}", auth=auth)
                            if resp_del.status_code in (200, 204):
                                st.success("J'aime supprimé")
                                st.experimental_rerun()
                            else:
                                st.error(f"Erreur suppression jaime : {resp_del.status_code} - {safe_json(resp_del)}")
                        except Exception as e:
                            st.error(f"Erreur lors de la suppression du jaime : {e}")
                else:
                    if st.button(f"🤍 J'aime", key=like_key):
                        try:
                            # API: POST /jaimes?id_activite=X
                            resp_post = requests.post(API_JAIMES, params={"id_activite": activity_id}, auth=auth)
                            if resp_post.status_code in (200,201):
                                st.success("J'aime ajouté")
                                st.experimental_rerun()
                            else:
                                st.error(f"Erreur ajout jaime : {resp_post.status_code} - {safe_json(resp_post)}")
                        except Exception as e:
                            st.error(f"Erreur lors de l'ajout du jaime : {e}")
            except Exception as e_like:
                st.error(f"Erreur 'Jaime' : {e_like}")

            st.write("---")

            # --- COMMENTS ---
            try:
                st.markdown("**Commentaires :**")
                resp_comments = requests.get(f"{API_COMMENTAIRES}/{activity_id}", auth=auth)
                if resp_comments.status_code == 200:
                    comments_list = resp_comments.json()
                    if not comments_list:
                        st.caption("Aucun commentaire pour l'instant.")
                    else:
                        for c in comments_list:
                            texte = c.get('commentaire') or c.get('texte') or ''
                            auteur = c.get('id_auteur') or c.get('auteur') or 'Inconnu'
                            date_c = c.get('date_commentaire') or c.get('date') or ''
                            st.caption(f"{auteur} — {date_c}")
                            st.markdown(f"> {texte}")
                else:
                    st.info("Impossible de récupérer les commentaires pour cette activité.")
            except Exception as e:
                st.error(f"Erreur récupération commentaires : {e}")

            st.markdown("**Ajouter un commentaire :**")
            comment_key = f"comment_text_{activity_id}"
            button_key = f"comment_btn_{activity_id}"
            commentaire_texte = st.text_area("Votre commentaire", key=comment_key, label_visibility="collapsed")
            if st.button("Envoyer", key=button_key):
                if not commentaire_texte or not commentaire_texte.strip():
                    st.warning("Le commentaire ne peut pas être vide.")
                else:
                    try:
                        resp_comment = requests.post(
                            API_COMMENTAIRES,
                            params={"id_activite": activity_id, "commentaire": commentaire_texte},
                            auth=auth
                        )
                        if resp_comment.status_code in (200,201):
                            st.success("Commentaire ajouté !")
                            st.experimental_rerun()
                        else:
                            st.error(f"Erreur lors de l'ajout du commentaire : {resp_comment.status_code} - {safe_json(resp_comment)}")
                    except Exception as e:
                        st.error(f"Erreur envoi commentaire : {e}")

            # --- DELETE (if allowed) ---
            if show_delete_button:
                st.divider()
                st.markdown("**Supprimer l'activité**")
                delete_key = f"delete_btn_{activity_id}"
                if st.button("Supprimer cette activité", key=delete_key):
                    try:
                        resp = requests.delete(f"{API_DELETE_ACTIVITE}/{activity_id}", auth=auth)
                        if resp.status_code in (200, 204):
                            st.success("Activité supprimée avec succès !")
                            # invalidate cache if any
                            if 'activites_list' in st.session_state:
                                del st.session_state['activites_list']
                            st.experimental_rerun()
                        else:
                            st.error(f"Erreur suppression activité : {resp.status_code} - {safe_json(resp)}")
                    except Exception as e:
                        st.error(f"Erreur suppression activité : {e}")

# --- 4. My activities ---
def afficher_activites_personnelles():
    st.subheader("Mes activités")
    if st.button("Afficher / Actualiser mes activités"):
        user_id = st.session_state["user_id"]
        auth = auth_tuple()
        try:
            resp = requests.get(f"{API_ACTIVITES}/{user_id}", auth=auth)
            if resp.status_code == 200:
                st.session_state['activites_list'] = resp.json()
            else:
                st.error(f"Erreur récupération activités : {resp.status_code} - {safe_json(resp)}")
                if 'activites_list' in st.session_state:
                    del st.session_state['activites_list']
        except Exception as e:
            st.error(f"Erreur requête activités : {e}")
            if 'activites_list' in st.session_state:
                del st.session_state['activites_list']

    if 'activites_list' in st.session_state:
        display_activity_list(st.session_state['activites_list'], show_delete_button=True)

# --- 5. Search profile ---
def afficher_recherche_profil():
    st.subheader("Rechercher un Utilisateur")
    pseudo_recherche = st.text_input("Entrer le pseudo de l'utilisateur", key="pseudo_search")

    if st.button("Rechercher"):
        if not pseudo_recherche:
            st.warning("Entrez un pseudo.")
            return
        # clear previous
        for k in ['profil_data', 'profil_activites', 'profil_suivi']:
            if k in st.session_state:
                del st.session_state[k]
        st.session_state['profil_recherche'] = pseudo_recherche

    if 'profil_recherche' in st.session_state:
        pseudo = st.session_state['profil_recherche']
        auth = auth_tuple()
        logged_in_user_id = st.session_state['user_id']
        try:
            if 'profil_data' not in st.session_state:
                resp = requests.get(f"{API_UTILISATEUR_PSEUDO}/{pseudo}", auth=auth)
                if resp.status_code == 200:
                    st.session_state['profil_data'] = resp.json()
                else:
                    st.error(f"Utilisateur '{pseudo}' non trouvé ({resp.status_code}).")
                    return
            profil_data = st.session_state['profil_data']
            profil_user_id = profil_data.get('id_utilisateur') or profil_data.get('id')

            col1, col2 = st.columns([3,1])
            with col1:
                st.markdown(f"#### Profil de **{profil_data.get('pseudo', '[inconnu]')}**")
                st.caption(f"Nom : {profil_data.get('nom','N/A')} {profil_data.get('prenom','')}")
            with col2:
                # Determine follow status by fetching followed list of logged in user
                if 'profil_suivi' not in st.session_state:
                    try:
                        resp_suivis = requests.get(f"{API_ABONNEMENTS_SUIVIS}/{logged_in_user_id}", auth=auth)
                        if resp_suivis.status_code == 200:
                            payload = resp_suivis.json()
                            # API returns a list of ids (set converted to list), e.g. [2,5,8]
                            if isinstance(payload, dict) and 'suivis' in payload:
                                suivis_list = payload.get('suivis', [])
                            elif isinstance(payload, (list, set, tuple)):
                                suivis_list = list(payload)
                            else:
                                # unknown format -> assume empty
                                suivis_list = []
                        else:
                            suivis_list = []
                        st.session_state['profil_suivi'] = profil_user_id in suivis_list
                    except Exception as e:
                        st.error(f"Erreur récupération suivis : {e}")
                        st.session_state['profil_suivi'] = False

                is_following = st.session_state['profil_suivi']

                if profil_user_id != logged_in_user_id:
                    if is_following:
                        if st.button("Se désabonner", key=f"follow_btn_{profil_user_id}"):
                            try:
                                # API: DELETE /abonnements?id_utilisateur_suivi=X (uses current user from auth to delete)
                                resp_del = requests.delete(API_ABONNEMENTS, params={"id_utilisateur_suivi": profil_user_id}, auth=auth)
                                if resp_del.status_code in (200,204):
                                    st.success("Désabonné")
                                    del st.session_state['profil_suivi']
                                    st.experimental_rerun()
                                else:
                                    st.error(f"Erreur désabonnement : {resp_del.status_code} - {safe_json(resp_del)}")
                            except Exception as e:
                                st.error(f"Erreur lors de la suppression de l'abonnement : {e}")
                    else:
                        if st.button("Suivre", key=f"follow_btn_{profil_user_id}"):
                            try:
                                # API: POST /abonnements?id_utilisateur_suivi=X
                                resp_post = requests.post(API_ABONNEMENTS, params={"id_utilisateur_suivi": profil_user_id}, auth=auth)
                                if resp_post.status_code in (200,201):
                                    st.success("Abonnement créé")
                                    if 'profil_suivi' in st.session_state:
                                        del st.session_state['profil_suivi']
                                    st.experimental_rerun()
                                else:
                                    st.error(f"Erreur abonnement : {resp_post.status_code} - {safe_json(resp_post)}")
                            except Exception as e:
                                st.error(f"Erreur lors de la création de l'abonnement : {e}")

            st.divider()
            # Activities of profile
            st.markdown(f"**Activités de {profil_data.get('pseudo','[inconnu]')}**")
            if 'profil_activites' not in st.session_state:
                try:
                    resp_acts = requests.get(f"{API_ACTIVITES}/{profil_user_id}", auth=auth)
                    if resp_acts.status_code == 200:
                        st.session_state['profil_activites'] = resp_acts.json()
                    else:
                        st.session_state['profil_activites'] = []
                except Exception as e:
                    st.error(f"Erreur récupération activités du profil : {e}")
                    st.session_state['profil_activites'] = []
            display_activity_list(st.session_state.get('profil_activites', []), show_delete_button=False)

        except Exception as e:
            st.error(f"Erreur lors de la récupération du profil : {e}")
            if 'profil_data' in st.session_state:
                del st.session_state['profil_data']

# --- 6. Stats ---
def afficher_statistiques_personnelles():
    st.subheader("Mes Statistiques Personnelles")
    auth = auth_tuple()
    user_id = st.session_state["user_id"]

    st.markdown("##### 📈 Statistiques Globales")
    if st.button("Afficher mes statistiques totales"):
        try:
            resp = requests.get(f"{API_STATS_TOTAL}/{user_id}", auth=auth)
            if resp.status_code == 200:
                st.session_state['total_stats'] = resp.json()
            else:
                st.error(f"Erreur récupération stats totales : {resp.status_code} - {safe_json(resp)}")
                if 'total_stats' in st.session_state:
                    del st.session_state['total_stats']
        except Exception as e:
            st.error(f"Erreur requête stats totales : {e}")
            if 'total_stats' in st.session_state:
                del st.session_state['total_stats']

    if 'total_stats' in st.session_state:
        stats_total = st.session_state['total_stats']
        # API returns: nombre_activites_total, distance_totale, duree_totale
        nb = stats_total.get('nombre_activites_total', {})
        dist = stats_total.get('distance_totale', {})
        duree = stats_total.get('duree_totale', {})
        # If the API gives aggregated dicts by sport, use as-is; else present totals
        if isinstance(nb, dict) and nb:
            st.markdown("**Nombre d'activités (par sport)**")
            st.bar_chart(nb)
        else:
            st.metric("Nombre total d'activités", f"{nb}")
        if isinstance(dist, dict) and dist:
            st.markdown("**Distance totale (km) par sport**")
            st.bar_chart(dist)
        else:
            st.metric("Distance totale (km)", f"{dist}")
        if isinstance(duree, dict) and duree:
            # assume duree may be seconds or minutes; try to normalize if keys indicate seconds
            # if numbers look large treat as seconds convert to minutes for display
            try:
                # attempt to convert dict values to minutes if they seem large
                sample = next(iter(duree.values()))
                if isinstance(sample, (int,float)) and sample > 1000:
                    duree_min = {k: v/60.0 for k,v in duree.items()}
                    st.markdown("**Durée totale (minutes) par sport**")
                    st.bar_chart(duree_min)
                else:
                    st.markdown("**Durée totale (minutes) par sport**")
                    st.bar_chart(duree)
            except Exception:
                st.write(duree)
        else:
            st.metric("Durée totale", f"{duree}")

    st.divider()
    st.markdown("##### 📅 Statistiques Hebdomadaires")
    date_ref = st.date_input("Choisir une date de référence pour la semaine")
    if st.button("Afficher les statistiques de la semaine"):
        date_str = date_ref.strftime("%Y-%m-%d")
        try:
            resp = requests.get(f"{API_STATS_SEMAINE}/{user_id}", params={"date_reference": date_str}, auth=auth)
            if resp.status_code == 200:
                st.session_state['weekly_stats'] = resp.json()
                st.session_state['weekly_stats_date'] = date_str
            else:
                st.error(f"Erreur récupération stats semaine : {resp.status_code} - {safe_json(resp)}")
                if 'weekly_stats' in st.session_state:
                    del st.session_state['weekly_stats']
        except Exception as e:
            st.error(f"Erreur requête stats semaine : {e}")
            if 'weekly_stats' in st.session_state:
                del st.session_state['weekly_stats']

    if 'weekly_stats' in st.session_state:
        s = st.session_state['weekly_stats']
        st.info(f"Affichage des statistiques pour la semaine du {st.session_state.get('weekly_stats_date','?')}")
        # API returns: nombre_activites_semaine, distance_semaine, duree_semaine
        nbw = s.get('nombre_activites_semaine', {})
        distw = s.get('distance_semaine', 0)
        dureew = s.get('duree_semaine', 0)
        try:
            duree_min = float(dureew) / 60.0 if dureew else 0.0
        except Exception:
            duree_min = dureew
        col3, col4 = st.columns(2)
        col3.metric("Distance (Semaine)", f"{distw:.2f} km" if isinstance(distw,(int,float)) else str(distw))
        col4.metric("Durée (Semaine)", f"{duree_min:.1f} minutes" if isinstance(duree_min,(int,float)) else str(duree_min))
        if isinstance(nbw, dict) and nbw:
            st.markdown("**Nombre d'activités (semaine) par sport**")
            st.bar_chart(nbw)

# --- Main layout ---
if not st.session_state["connected"]:
    auth_form()
else:
    tab1, tab2, tab3, tab4 = st.tabs(["Poster Activité", "Mes Activités", "Mes Statistiques", "Rechercher Profil"])

    with tab1:
        gpx_analyse_et_creation()

    with tab2:
        afficher_activites_personnelles()

    with tab3:
        afficher_statistiques_personnelles()

    with tab4:
        afficher_recherche_profil()
