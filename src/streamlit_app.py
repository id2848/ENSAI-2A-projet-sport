import streamlit as st
import requests
import pandas as pd

API_ME = "http://localhost:9876/me"
API_GPX = "http://localhost:9876/upload-gpx"

if 'connected' not in st.session_state:
    st.session_state['connected'] = False

st.title("Connexion ")

# 1. Authentification
def auth_form():
    st.subheader("Identification")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Me connecter"):
        try:
            resp = requests.get(API_ME, auth=(username, password))
            if resp.status_code == 200:
                st.session_state['connected'] = True
                st.session_state['username'] = username
                st.session_state['password'] = password
                st.success("Connecté !")
            else:
                st.error("Identifiants incorrects")
        except Exception as e:
            st.error(f"Erreur de connexion : {e}")

# 2. Upload et analyse GPX + graphique simple
def gpx_analyse():
    st.success(f"Connecté en tant que {st.session_state['username']}")
    st.subheader("Analyse de fichier GPX & Statistiques")
    uploaded_file = st.file_uploader("Choisir un fichier GPX", type=["gpx"])
    if uploaded_file is not None:
        if st.button("Analyser le fichier"):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/gpx+xml")}
            with st.spinner("Analyse en cours..."):
                try:
                    resp = requests.post(
                        API_GPX,
                        files=files,
                        auth=(st.session_state['username'], st.session_state['password'])
                    )
                    resp.raise_for_status()
                    data = resp.json()
                    st.success("Analyse terminée ✅")
                    # Utilise directement le dictionnaire retourné
                    activite = data.get("activite", data)
                    st.subheader("Résumé activité")
                    st.write(f"Nom : {activite.get('nom', '[inconnu]')}")
                    st.write(f"Type : {activite.get('type', '[inconnu]')}")
                    st.write(f"Distance totale (km) : {activite.get('distance totale', '[inconnu]')}")
                    st.write(f"Durée totale (min) : {activite.get('durée totale', '[inconnu]')}")
                    st.write(f"Vitesse moyenne (km/h) : {activite.get('vitesse moyenne', '[inconnu]')}")
                except Exception as e:
                    st.error(f"Erreur de requête : {e}")

if not st.session_state['connected']:
    auth_form()
else:
    gpx_analyse()

API_ACTIVITES = "http://localhost:9876/activites/"


if st.session_state.get('connected'):
    st.success(f"Connecté en tant que {st.session_state['username']}")
    # Nouvelle section : afficher toutes les activités
    if st.button("Afficher toutes mes activités"):
        user_id = st.session_state['username']  # ou l'id réel si tu le stockes
        resp = requests.get(
            f"{API_ACTIVITES}{user_id}",
            auth=(st.session_state['username'], st.session_state['password'])
        )
        if resp.status_code == 200:
            activites = resp.json()
            if activites:
                st.subheader("Mes activités")
                df = pd.DataFrame(activites)
                st.dataframe(df)
            else:
                st.info("Aucune activité trouvée.")
        else:
            st.error("Erreur de récupération des activités.")
