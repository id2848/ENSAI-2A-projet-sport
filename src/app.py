from fastapi.responses import RedirectResponse
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from fastapi import FastAPI, UploadFile, File, HTTPException
import io

import logging
from utils.log_init import initialiser_logs

from service.activite_service import ActiviteService

from utils.parse_strava_gpx import parse_strava_gpx

# --- Configuration ---

app = FastAPI(title="Webservice Sports ENSAI")

initialiser_logs("Webservice")

# Authentification basique

security = HTTPBasic()

USERS = {
    "alice": {"password": "wonderland", "roles": ["admin"]},
    "bob":   {"password": "builder",    "roles": ["user"]},
}

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password

    user = USERS.get(username)
    if not user or not secrets.compare_digest(password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return {"username": username, "roles": user["roles"]}

@app.get("/me")
def me(user = Depends(get_current_user)):
    return {"user": user}

# ----------------------------------------------------------

# --- Endpoints de base ---
@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirige vers la documentation de l'API."""
    return RedirectResponse(url="/docs")

# --- Endpoints Gestion des activités ---
@app.get("/activites/{id_utilisateur}")
def activites_par_utilisateur(id_utilisateur: int, user = Depends(get_current_user)):
    """Lister les activités d'un utilisateur donné."""
    return ActiviteService().lister_activites(id_utilisateur)

@app.post("/activites")
async def creer_activite(file: UploadFile = File(...), sport: str = "randonnée", user = Depends(get_current_user)):
    """Créer une nouvelle activité avec un fichier GPX."""
    content = await file.read()
    activite = parse_strava_gpx(content, sport)
    ActiviteService().creer_activite(user["username"], activite)
    return {"message": "Activité créée", "activite": activite}

@app.put("/activites/{id_activite}")
def modifier_activite(id_activite: int, sport: str, user = Depends(get_current_user)):
    """Modifier une activité existante."""
    updated_activite = ActiviteService().modifier_activite(id_activite, sport)
    if not updated_activite:
        raise HTTPException(status_code=404, detail="Activité non trouvée")
    return {"message": "Activité modifiée", "activite": updated_activite}

@app.delete("/activites/{id_activite}")
def supprimer_activite(id_activite: int, user = Depends(get_current_user)):
    """Supprimer une activité."""
    success = ActiviteService().supprimer_activite(id_activite)
    if not success:
        raise HTTPException(status_code=404, detail="Activité non trouvée")
    return {"message": "Activité supprimée"}

# --- Endpoints Interactions avec les activités ---
@app.post("/jaimes")
def ajouter_jaime(id_activite: int, user = Depends(get_current_user)):
    """L'utilisateur ajoute un jaime à une activité."""
    Jaime = ActiviteService().ajouter_jaime(user["username"], id_activite)
    return {"message": "Like ajouté", "jaime": Jaime}

@app.delete("/jaimes/{id_activite}/{id_utilisateur}")
def supprimer_jaime(id_activite: int, id_utilisateur: int, user = Depends(get_current_user)):
    """L'utilisateur supprime son jaime d'une activité."""
    ActiviteService().supprimer_jaime(id_activite, id_utilisateur)
    return {"message": "Like supprimé"}

@app.post("/commentaires")
def ajouter_commentaire(id_activite: int, commentaire: str, user = Depends(get_current_user)):
    """Ajouter un commentaire à une activité."""
    commentaire_objet = ActiviteService().ajouter_commentaire(user["username"], id_activite, commentaire)
    return {"message": "Commentaire ajouté", "commentaire": commentaire_objet}

@app.delete("/commentaires/{id_commentaire}")
def supprimer_commentaire(id_commentaire: int, user = Depends(get_current_user)):
    """Supprimer un commentaire."""
    ActiviteService().supprimer_commentaire(id_commentaire)
    return {"message": "Commentaire supprimé"}

# --- Endpoints Abonnements ---
@app.post("/abonnements")
def creer_abonnement(id_utilisateur_suiveur: int, id_utilisateur_suivi: int, user = Depends(get_current_user)):
    """S'abonner à un utilisateur."""
    AbonnementService().creer_abonnement(id_utilisateur_suiveur, id_utilisateur_suivi)
    return {"message": "Abonnement créé"}

@app.delete("/abonnements")
def supprimer_abonnement(id_utilisateur_suiveur: int, id_utilisateur_suivi: int, user = Depends(get_current_user)):
    """Se désabonner d'un utilisateur."""
    AbonnementService().supprimer_abonnement(id_utilisateur_suiveur, id_utilisateur_suivi)
    return {"message": "Abonnement supprimé"}

@app.get("/abonnements/suivis/{id_utilisateur}")
def lister_abonnements_suivis(id_utilisateur: int, user = Depends(get_current_user)):
    """Lister les utilisateurs suivis."""
    suivis = AbonnementService().lister_utilisateurs_suivis(id_utilisateur)
    return {"suivis": suivis}

@app.get("/abonnements/suiveurs/{id_utilisateur}")
def lister_abonnements_suiveurs(id_utilisateur: int, user = Depends(get_current_user)):
    """Lister les utilisateurs qui suivent l'utilisateur."""
    suiveurs = AbonnementService().lister_utilisateurs_suiveurs(id_utilisateur)
    return {"suiveurs": suiveurs}

# --- Endpoints Fil d'actualité ---
@app.get("/fil-dactualite/{id_utilisateur}")
def fil_dactualite(id_utilisateur: int, user = Depends(get_current_user)):
    """Afficher le fil d'actualités de l'utilisateur."""
    activites = ServiceFilDactualite().creer_fil_dactualite(id_utilisateur)
    return {"fil_dactualite": activites}

# --- Endpoints Statistiques ---
@app.get("/statistiques/activites/{id_utilisateur}")
def statistiques_activites(id_utilisateur: int, user = Depends(get_current_user)):
    """Statistiques des activités d'un utilisateur (par semaine et par sport)."""
    activites_count = ServiceStatistiques().calculer_nombre_activites(id_utilisateur)
    return {"nombre_activites": activites_count}

@app.get("/statistiques/hebdomadaire/{id_utilisateur}")
def statistiques_hebdomadaire(id_utilisateur: int, user = Depends(get_current_user)):
    """Statistiques hebdomadaires détaillées de l'utilisateur."""
    # A METTRE A JOUR
    activites = ServiceStatistiques().calculer_distance_totale(id_utilisateur)
    duree = ServiceStatistiques().calculer_duree_totale(id_utilisateur)
    return {"distance_totale": activites, "duree_totale": duree}

# --- Endpoint Upload GPX ---
@app.post("/upload-gpx")
async def upload_gpx(file: UploadFile = File(...)):
    """Upload et parsing d'un fichier GPX."""
    content = await file.read()
    parsed_activite = parse_strava_gpx(content)
    return {"message": "Fichier GPX analysé", "activite": parsed_activite}


# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9876)

    logging.info("Arret du Webservice")
