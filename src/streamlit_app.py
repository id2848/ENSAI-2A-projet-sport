import streamlit as st
import requests
from typing import Any, List
from datetime import datetime

# --- URLs API ---
API_BASE = "http://localhost:9876"
API_ME = f"{API_BASE}/me"
API_ACTIVITES = f"{API_BASE}/activites"
API_ACTIVITES_FILTRES = f"{API_BASE}/activites-filtres"
API_DELETE_ACTIVITE = f"{API_BASE}/activites"
API_COMMENTAIRES = f"{API_BASE}/commentaires"
API_UPLOAD_GPX = f"{API_BASE}/upload-gpx"
API_UTILISATEUR_PSEUDO = f"{API_BASE}/utilisateurs/pseudo"
API_UTILISATEUR_ID = f"{API_BASE}/utilisateurs"
API_ABONNEMENTS = f"{API_BASE}/abonnements"
API_ABONNEMENTS_SUIVIS = f"{API_BASE}/abonnements/suivis"
API_JAIMES = f"{API_BASE}/jaimes"
API_JAIMES_EXISTE = f"{API_BASE}/jaimes/existe"
API_JAIMES_COMPTER = f"{API_BASE}/jaimes/compter"
API_STATS_TOTAL = f"{API_BASE}/statistiques/total"
API_STATS_SEMAINE = f"{API_BASE}/statistiques/semaine"
API_INSCRIPTION = f"{API_BASE}/inscription"
API_FIL = f"{API_BASE}/fil-dactualite"

# --- Initialisation Session ---
if "connected" not in st.session_state:
    st.session_state["connected"] = False
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "username" not in st.session_state:
    st.session_state["username"] = None
if "password" not in st.session_state:
    st.session_state["password"] = None

st.set_page_config(page_title="Réseau social Sports ENSAI", layout="wide")
st.title("Réseau social Sports ENSAI")


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
    a = {}
    a["id_activite"] = extract_activity_field(
        activite_raw, "id_activite", "id", "id_activity", default=None
    )
    a["sport"] = extract_activity_field(
        activite_raw, "sport", "type", default="inconnu"
    )
    a["id_utilisateur"] = extract_activity_field(
        activite_raw, "id_utilisateur", "id_auteur", default=None
    )

    dist = extract_activity_field(
        activite_raw,
        "distance",
        "distance totale",
        "distance_km",
        "distance_m",
        default=None,
    )
    if isinstance(dist, str):
        try:
            dist = float(dist.replace(",", "."))
        except Exception:
            dist = None
    if isinstance(dist, (int, float)):
        if (
            dist > 1000
        ):  # Heuristique: si > 1000, c'est surement en mètres (mais normalement km)
            dist = dist / 1000.0
    a["distance"] = dist if dist is not None else 0.0

    duree = extract_activity_field(
        activite_raw,
        "duree",
        "durée totale",
        "duree_minutes",
        "duree_secondes",
        default=None,
    )
    if isinstance(duree, str):
        try:
            duree = float(duree.replace(",", "."))
        except Exception:
            duree = None
    if isinstance(duree, (int, float)):
        # Si très grand, supposé en secondes (mais normalement minutes)
        if duree > 10000:
            duree = duree / 60.0
    a["duree"] = duree if duree is not None else 0.0

    a["date"] = extract_activity_field(
        activite_raw, "date", "date_activite", "start_time", default=None
    )
    a["nom"] = extract_activity_field(activite_raw, "nom", "name", default="")
    return a


# --- 1. Authentification et Inscription ---
def auth_screen():
    tab_conn, tab_insc = st.tabs(["Connexion", "Inscription"])

    with tab_conn:
        st.subheader("Connexion")
        username = st.text_input("Nom d'utilisateur", key="login_user")
        password = st.text_input("Mot de passe", type="password", key="login_pass")
        if st.button("Se connecter"):
            try:
                resp = requests.get(API_ME, auth=(username, password))
                if resp.status_code == 200:
                    user = resp.json()
                    uid = user.get("id_utilisateur") or user.get("id")
                    if uid is None:
                        st.error("L'API /me n'a pas retourné d'ID utilisateur.")
                        return
                    st.session_state["username"] = username
                    st.session_state["password"] = password
                    st.session_state["user_id"] = uid
                    st.session_state["connected"] = True
                    st.success("Connecté avec succès !")
                    st.rerun()
                else:
                    st.error("Identifiants invalides.")
            except Exception as e:
                st.error(f"Erreur de connexion : {e}")

    with tab_insc:
        st.subheader("Créer un compte")
        new_pseudo = st.text_input("Pseudo *", key="insc_pseudo")
        new_mdp = st.text_input("Mot de passe *", type="password", key="insc_mdp")
        new_nom = st.text_input("Nom", key="insc_nom")
        new_prenom = st.text_input("Prénom", key="insc_prenom")
        new_date = st.date_input(
            "Date de naissance",
            key="insc_date",
            min_value=datetime(1900, 1, 1),
            max_value=datetime.today(),
        )
        new_sexe = st.text_input("Sexe", key="insc_sexe")

        if st.button("S'inscrire"):
            if not new_pseudo or not new_mdp:
                st.warning("Le pseudo et le mot de passe sont obligatoires.")
            else:
                payload = {
                    "pseudo": new_pseudo,
                    "mot_de_passe": new_mdp,
                    "nom": new_nom,
                    "prenom": new_prenom,
                    "date_de_naissance": new_date.strftime("%Y-%m-%d"),
                    "sexe": new_sexe,
                }
                try:
                    # Note: FastAPI attend des query params selon définition dans app.py
                    # Utilisation de params=payload pour envoyer en query string
                    resp = requests.post(API_INSCRIPTION, params=payload)
                    if resp.status_code == 200:
                        st.success(
                            "Compte créé ! Vous pouvez maintenant vous connecter."
                        )
                    else:
                        st.error(
                            f"Erreur inscription : {resp.status_code} - {safe_json(resp)}"
                        )
                except Exception as e:
                    st.error(f"Erreur technique : {e}")


def logout_button():
    if st.sidebar.button("Se déconnecter"):
        st.session_state["connected"] = False
        st.session_state["username"] = None
        st.session_state["password"] = None
        st.session_state["user_id"] = None
        st.rerun()


# --- 2. GPX upload ---
def gpx_analyse_et_creation():
    st.subheader("Importer une activité (GPX)")
    uploaded_file = st.file_uploader("Choisir un fichier GPX", type=["gpx"])
    if uploaded_file is not None:
        if st.button("Analyser le fichier"):
            uploaded_file.seek(0)
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/gpx+xml",
                )
            }
            try:
                resp = requests.post(API_UPLOAD_GPX, files=files)
                if resp.status_code == 200:
                    data = resp.json()
                    activite = data.get("activite", data)
                    st.session_state["analyse_data"] = activite
                    st.session_state["uploaded_file_bytes"] = uploaded_file.getvalue()
                    st.session_state["uploaded_file_name"] = uploaded_file.name
                    st.success("Analyse réussie.")
                else:
                    st.error(f"Erreur d'analyse : {resp.status_code}")
            except Exception as e:
                st.error(f"Erreur : {e}")

    if "analyse_data" in st.session_state:
        st.markdown("#### Résumé")
        activite = st.session_state["analyse_data"]
        st.write(f"**Type :** {activite.get('type', '?')}")
        st.write(f"**Distance :** {activite.get('distance totale', '?')} km")
        st.write(f"**Durée :** {activite.get('durée totale', '?')} min")
        sport = st.selectbox(
            "Confirmer le sport", ["course", "vélo", "randonnée", "natation", "autre"]
        )
        if st.button("Poster cette activité"):
            files_create = {
                "file": (
                    st.session_state["uploaded_file_name"],
                    st.session_state["uploaded_file_bytes"],
                    "application/gpx+xml",
                )
            }
            try:
                resp = requests.post(
                    API_ACTIVITES,
                    files=files_create,
                    params={"sport": sport},
                    auth=auth_tuple(),
                )
                if resp.status_code == 200:
                    st.success("Activité postée !")
                    del st.session_state["analyse_data"]
                    st.rerun()
                else:
                    st.error(f"Erreur lors de la création : {resp.text}")
            except Exception as e:
                st.error(f"Erreur : {e}")


# --- 3. Afficher les Activités ---
def display_activity_list(
    activites_list: List[dict], show_delete_button: bool = False, key_prefix: str = ""
):
    if not activites_list:
        st.info("Aucune activité à afficher.")
        return

    auth = auth_tuple()
    logged_in_user_id = st.session_state["user_id"]

    for raw in activites_list:
        a = normalize_activity(raw)
        activity_id = a.get("id_activite")

        if not activity_id:
            continue

        # --- RÉCUPÉRER LE PSEUDO DE L'AUTEUR ---
        auteur_id = a.get("id_utilisateur")
        pseudo_auteur = auteur_id  # fallback si erreur

        try:
            resp_user = requests.get(f"{API_UTILISATEUR_ID}/{auteur_id}", auth=auth)
            if resp_user.status_code == 200:
                pseudo_auteur = resp_user.json().get("pseudo", auteur_id)
        except Exception:
            pass

        expander_label = f"**{pseudo_auteur}** - {a.get('sport', 'Activité')} - {a.get('date','')} ({a.get('distance',0)} km)"
        with st.expander(expander_label):
            col_a, col_b = st.columns(2)
            with col_a:
                st.write(f"**Sport :** {a.get('sport')}")
                st.write(f"**Distance :** {a.get('distance')} km")
            with col_b:
                st.write(f"**Durée :** {a.get('duree')} min")
                if a.get("duree", 0) > 0:
                    vitesse = float(a["distance"]) / (float(a["duree"]) / 60)
                    st.write(f"**Vitesse :** {vitesse:.2f} km/h")

            st.divider()

            # --- LIKES ---
            col_l1, col_l2 = st.columns([1, 5])

            nb_likes = 0
            try:
                resp_count = requests.get(
                    API_JAIMES_COMPTER, params={"id_activite": activity_id}, auth=auth
                )
                if resp_count.status_code == 200:
                    nb_likes = resp_count.json().get("nombre_jaimes", 0)
            except Exception:
                pass

            user_has_liked = False
            try:
                resp_exist = requests.get(
                    API_JAIMES_EXISTE,
                    params={"id_activite": activity_id, "id_auteur": logged_in_user_id},
                    auth=auth,
                )
                if resp_exist.status_code == 200:
                    user_has_liked = bool(resp_exist.json())
            except Exception:
                pass

            with col_l1:
                like_btn_key = f"{key_prefix}btn_like_{activity_id}"

                if user_has_liked:
                    if st.button("❤️", key=like_btn_key, help="Je n'aime plus"):
                        try:
                            requests.delete(f"{API_JAIMES}/{activity_id}", auth=auth)
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))
                else:
                    if st.button("🤍", key=like_btn_key, help="J'aime"):
                        try:
                            requests.post(
                                API_JAIMES,
                                params={"id_activite": activity_id},
                                auth=auth,
                            )
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))
            with col_l2:
                st.markdown(f"**{nb_likes}** J'aime")

            # --- COMMENTAIRES ---
            st.markdown("#### Commentaires")
            try:
                resp_com = requests.get(f"{API_COMMENTAIRES}/{activity_id}", auth=auth)
                if resp_com.status_code == 200:
                    for c in resp_com.json():
                        contenu = c.get("contenu") or ""
                        auteur_id = c.get("id_auteur")
                        date_com = c.get("date_commentaire")

                        pseudo = auteur_id  # fallback si erreur
                        try:
                            resp_user = requests.get(
                                f"{API_UTILISATEUR_ID}/{auteur_id}", auth=auth
                            )
                            if resp_user.status_code == 200:
                                pseudo = resp_user.json().get("pseudo", auteur_id)
                        except Exception:
                            pass  # On garde l'ID si erreur API

                        st.markdown(f"👤 **{pseudo}** ({date_com}) : {contenu}")
                else:
                    st.caption("Pas de commentaires.")
            except Exception:
                st.caption("Erreur chargement commentaires.")

            txt_com = st.text_input(
                "Écrire un commentaire...", key=f"{key_prefix}input_com_{activity_id}"
            )
            if st.button("Envoyer", key=f"{key_prefix}send_com_{activity_id}"):
                if txt_com:
                    requests.post(
                        API_COMMENTAIRES,
                        params={"id_activite": activity_id, "commentaire": txt_com},
                        auth=auth,
                    )
                    st.success("Envoyé !")
                    st.rerun()

            # --- DELETE ---
            if show_delete_button:
                st.divider()
                if st.button(
                    "Supprimer l'activité", key=f"{key_prefix}del_act_{activity_id}"
                ):
                    requests.delete(f"{API_DELETE_ACTIVITE}/{activity_id}", auth=auth)
                    st.success("Supprimé")
                    st.rerun()


# --- 4. Fil d'actualité ---
def afficher_fil_dactualite():
    st.subheader("Fil d'actualité")
    user_id = st.session_state["user_id"]
    auth = auth_tuple()

    if st.button("Actualiser le fil"):
        try:
            # Appel à l'endpoint GET /fil-dactualite/{id}
            resp = requests.get(f"{API_FIL}/{user_id}", auth=auth)
            if resp.status_code == 200:
                st.session_state["fil_actu"] = resp.json()
            else:
                st.warning("Impossible de récupérer le fil ou fil vide.")
                st.session_state["fil_actu"] = []
        except Exception as e:
            st.error(f"Erreur : {e}")

    if "fil_actu" in st.session_state:
        display_activity_list(
            st.session_state["fil_actu"], show_delete_button=False, key_prefix="fil_"
        )


# --- 5. Mes Activités ---
def afficher_activites_personnelles():
    st.subheader("Mes activités")
    user_id = st.session_state["user_id"]

    # Champs de filtre (facultatifs)
    sport = st.selectbox(
        "Filtrer par sport (optionnel)",
        ["", "course", "vélo", "randonnée", "natation", "autre"],
    )
    date_debut = st.date_input("Date début (optionnel)", value=None)
    date_fin = st.date_input("Date fin (optionnel)", value=None)

    if st.button("Actualiser mes activités"):

        # Construction dynamique des paramètres
        params = {}
        if sport:
            params["sport"] = sport
        if date_debut:
            params["date_debut"] = date_debut.strftime("%Y-%m-%d")
        if date_fin:
            params["date_fin"] = date_fin.strftime("%Y-%m-%d")

        resp = requests.get(
            f"{API_ACTIVITES_FILTRES}/{user_id}", params=params, auth=auth_tuple()
        )

        if resp.status_code == 200:
            st.session_state["mes_activites"] = resp.json()
        else:
            st.error("Erreur lors du chargement des activités.")

    # Affichage si données déjà en session
    if "mes_activites" in st.session_state:
        display_activity_list(
            st.session_state["mes_activites"],
            show_delete_button=True,
            key_prefix="mes-",
        )


# --- 6. Recherche Profil ---
def afficher_recherche_profil():
    st.subheader("Rechercher un profil")
    pseudo = st.text_input("Pseudo")
    if st.button("Rechercher"):
        resp = requests.get(f"{API_UTILISATEUR_PSEUDO}/{pseudo}", auth=auth_tuple())
        if resp.status_code == 200:
            st.session_state["profil_trouve"] = resp.json()
            # Charger ses activités
            uid = resp.json()["id_utilisateur"]
            r2 = requests.get(f"{API_ACTIVITES}/{uid}", auth=auth_tuple())
            if r2.status_code == 200:
                st.session_state["profil_activites"] = r2.json()
        else:
            st.error("Utilisateur introuvable.")

    if "profil_trouve" in st.session_state:
        profil = st.session_state["profil_trouve"]
        st.markdown(f"### Profil de {profil['pseudo']}")
        st.write(f"Nom : {profil.get('prenom')} {profil.get('nom')}")

        # Bouton Suivre / Ne plus suivre
        current_uid = st.session_state["user_id"]
        target_uid = profil["id_utilisateur"]

        if current_uid != target_uid:
            # Vérifier abonnement
            is_following = False
            try:
                # On récupère la liste des suivis pour vérifier
                r_suivis = requests.get(
                    f"{API_ABONNEMENTS_SUIVIS}/{current_uid}", auth=auth_tuple()
                )
                if r_suivis.status_code == 200:
                    suivis = r_suivis.json()  # liste d'IDs
                    if target_uid in suivis:
                        is_following = True
            except Exception:
                pass

            if is_following:
                if st.button("Se désabonner"):
                    requests.delete(
                        API_ABONNEMENTS,
                        params={"id_utilisateur_suivi": target_uid},
                        auth=auth_tuple(),
                    )
                    st.success("Désabonné")
                    st.rerun()
            else:
                if st.button("Suivre"):
                    requests.post(
                        API_ABONNEMENTS,
                        params={"id_utilisateur_suivi": target_uid},
                        auth=auth_tuple(),
                    )
                    st.success("Abonné !")
                    st.rerun()

        st.divider()
        st.markdown("**Activités récentes**")
        if "profil_activites" in st.session_state:
            display_activity_list(
                st.session_state["profil_activites"],
                show_delete_button=False,
                key_prefix="recherche_",
            )


# --- 7. Statistiques ---
def afficher_statistiques():
    st.subheader("Mes Statistiques Personnelles")
    auth = auth_tuple()
    user_id = st.session_state["user_id"]

    st.markdown("##### 📈 Statistiques Globales")
    if st.button("Afficher mes statistiques totales"):
        try:
            resp = requests.get(f"{API_STATS_TOTAL}/{user_id}", auth=auth)
            if resp.status_code == 200:
                st.session_state["total_stats"] = resp.json()
            else:
                st.error(
                    f"Erreur récupération stats totales : {resp.status_code} - {safe_json(resp)}"
                )
                if "total_stats" in st.session_state:
                    del st.session_state["total_stats"]
        except Exception as e:
            st.error(f"Erreur requête stats totales : {e}")
            if "total_stats" in st.session_state:
                del st.session_state["total_stats"]

    if "total_stats" in st.session_state:
        stats_total = st.session_state["total_stats"]
        # API renvoie: nombre_activites_total, distance_totale, duree_totale
        nb = stats_total.get("nombre_activites_total", {})
        dist = stats_total.get("distance_totale", 0)
        duree = stats_total.get("duree_totale", 0)
        duree_min = float(duree) / 60.0 if duree else 0.0

        col1, col2 = st.columns(2)
        col1.metric("Distance totale (km)", f"{dist} km")
        col2.metric("Durée totale", f"{duree_min} minutes")

        if isinstance(nb, dict) and nb:
            st.markdown("**Nombre d'activités (par sport)**")
            st.bar_chart(nb)
        else:
            st.metric("Nombre total d'activités", f"{nb}")

    st.divider()
    st.markdown("##### 📅 Statistiques Hebdomadaires")
    date_ref = st.date_input("Choisir une date de référence pour la semaine")
    if st.button("Afficher les statistiques de la semaine"):
        date_str = date_ref.strftime("%Y-%m-%d")
        try:
            resp = requests.get(
                f"{API_STATS_SEMAINE}/{user_id}",
                params={"date_reference": date_str},
                auth=auth,
            )
            if resp.status_code == 200:
                st.session_state["weekly_stats"] = resp.json()
                st.session_state["weekly_stats_date"] = date_str
            else:
                st.error(
                    f"Erreur récupération stats semaine : {resp.status_code} - {safe_json(resp)}"
                )
                if "weekly_stats" in st.session_state:
                    del st.session_state["weekly_stats"]
        except Exception as e:
            st.error(f"Erreur requête stats semaine : {e}")
            if "weekly_stats" in st.session_state:
                del st.session_state["weekly_stats"]

    if "weekly_stats" in st.session_state:
        s = st.session_state["weekly_stats"]
        st.info(
            f"Affichage des statistiques pour la semaine du {st.session_state.get('weekly_stats_date','?')}"
        )
        # API renvoie: nombre_activites_semaine, distance_semaine, duree_semaine
        nbw = s.get("nombre_activites_semaine", {})
        distw = s.get("distance_semaine", 0)
        dureew = s.get("duree_semaine", 0)
        try:
            duree_min = float(dureew) / 60.0 if dureew else 0.0
        except Exception:
            duree_min = dureew
        col3, col4 = st.columns(2)
        col3.metric(
            "Distance (Semaine)",
            f"{distw:.2f} km" if isinstance(distw, (int, float)) else str(distw),
        )
        col4.metric(
            "Durée (Semaine)",
            (
                f"{duree_min:.1f} minutes"
                if isinstance(duree_min, (int, float))
                else str(duree_min)
            ),
        )
        if isinstance(nbw, dict) and nbw:
            st.markdown("**Nombre d'activités (semaine) par sport**")
            st.bar_chart(nbw)


# --- Main ---
if not st.session_state["connected"]:
    auth_screen()
else:
    logout_button()
    st.sidebar.markdown(f"Connecté : **{st.session_state['username']}**")

    tab_fil, tab_mes_acts, tab_poster, tab_profil, tab_stats = st.tabs(
        [
            "Fil d'actualité",
            "Mes Activités",
            "Poster (GPX)",
            "Rechercher Profil",
            "Statistiques",
        ]
    )

    with tab_fil:
        afficher_fil_dactualite()
    with tab_mes_acts:
        afficher_activites_personnelles()
    with tab_poster:
        gpx_analyse_et_creation()
    with tab_profil:
        afficher_recherche_profil()
    with tab_stats:
        afficher_statistiques()
