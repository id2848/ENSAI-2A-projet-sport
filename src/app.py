from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from fastapi import FastAPI, UploadFile, File, HTTPException
import io

import logging
from utils.log_init import initialiser_logs

from service.activite_service import ActiviteService
from service.service_statistiques import ServiceStatistiques
from service.utilisateur_service import UtilisateurService

from utils.gpx_parser import parse_gpx

# --- Configuration ---

app = FastAPI(title="Webservice Sports ENSAI")

initialiser_logs("Webservice")

# Authentification basique

security = HTTPBasic()

USERS = {
    "alice": {"id_utilisateur": 991, "password": "wonderland", "prenom": "Alice"},
    "bob":   {"id_utilisateur": 992, "password": "builder", "prenom": "Bob"},
}

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password

    #utilisateur = UtilisateurService().se_connecter(username, password)
    #if not utilisateur:
    user = USERS.get(username)
    if not user or not secrets.compare_digest(password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
        )
    #return utilisateur
    return user

# ----------------------------------------------------------

# --- Endpoints Authentification ---

@app.get("/me")
def me(user = Depends(get_current_user)):
    return user

@app.get("/logout")
async def logout(creds: HTTPBasicCredentials = Depends(get_current_user)):
    return HTMLResponse(content="Vous vous êtes déconnecté", status_code=status.HTTP_401_UNAUTHORIZED)


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
    """Créer une nouvelle activité avec un fichier GPX pour l'utilisateur connecté."""
    content = await file.read()
    try:
        parsed_activite = parse_gpx(content)
    except Exception as e:
        logging.error(f"Erreur lors du parsing du fichier GPX : {e}")
        return {"message": "Erreur lors du parsing du fichier GPX"}
    date_activite = parsed_activite["date"]
    distance = parsed_activite["distance totale"]
    duree = parsed_activite["durée totale"]
    success = ActiviteService().creer_activite(user["id_utilisateur"], sport, date_activite, distance, duree)
    return {"succès": success}

@app.put("/activites/{id_activite}")
def modifier_activite(id_activite: int, sport: str, user = Depends(get_current_user)):
    """Modifier une activité existante appartenant à l'utilisateur connecté."""
    activite = ActiviteService().trouver_activite_par_id(id_activite)
    if not activite:
        return {"message": "Cette activité n'existe pas"}
    if not activite.id_utilisateur == user["id_utilisateur"]:
        return {"message": "Cette activité ne vous appartient pas"}
    updated_activite = ActiviteService().modifier_activite(id_activite, sport)
    if not updated_activite:
        raise HTTPException(status_code=404, detail="Activité non trouvée")
    return {"message": "Activité modifiée", "activite": updated_activite}

@app.delete("/activites/{id_activite}")
def supprimer_activite(id_activite: int, user = Depends(get_current_user)):
    """Supprimer une activité appartenant à l'utilisateur connecté."""
    activite = ActiviteService().trouver_activite_par_id(id_activite)
    if not activite:
        return {"message": "Cette activité n'existe pas"}
    if not activite.id_utilisateur == user["id_utilisateur"]:
        return {"message": "Cette activité ne vous appartient pas"}
    success = ActiviteService().supprimer_activite(id_activite)
    if not success:
        raise HTTPException(status_code=404, detail="Activité non trouvée")
    return {"message": "Activité supprimée"}


# --- Endpoints Interactions avec les activités ---

@app.post("/jaimes")
def ajouter_jaime(id_activite: int, user = Depends(get_current_user)):
    """Ajouter un jaime à une activité pour l'utilisateur connecté."""
    Jaime = ActiviteService().ajouter_jaime(user["id_utilisateur"], id_activite)
    return {"message": "Jaime ajouté", "jaime": Jaime}

@app.delete("/jaimes/{id_activite}/{id_utilisateur}")
def supprimer_jaime(id_activite: int, user = Depends(get_current_user)):
    """Supprimer le jaime appartenant à l'utilisateur connecté d'une activité."""
    ActiviteService().supprimer_jaime(id_activite, user["id_utilisateur"])
    return {"message": "Jaime supprimé"}

@app.post("/commentaires")
def ajouter_commentaire(id_activite: int, commentaire: str, user = Depends(get_current_user)):
    """Ajouter un commentaire à une activité pour l'utilisateur connecté."""
    commentaire_objet = ActiviteService().ajouter_commentaire(user["id_utilisateur"], id_activite, commentaire)
    return {"message": "Commentaire ajouté", "commentaire": commentaire_objet}

@app.delete("/commentaires/{id_commentaire}")
def supprimer_commentaire(id_commentaire: int, user = Depends(get_current_user)):
    """Supprimer un commentaire appartenant à l'utilisateur connecté."""
    commentaire = ActiviteService().trouver_commentaire_par_id(id_commentaire)
    if not commentaire:
        return {"message": "Ce commentaire n'existe pas"}
    if not commentaire.id_auteur == user["id_utilisateur"]:
        return {"message": "Ce commentaire ne vous appartient pas"}
    ActiviteService().supprimer_commentaire(id_commentaire)
    return {"message": "Commentaire supprimé"}


# --- Endpoints Abonnements ---

@app.post("/abonnements")
def creer_abonnement(id_utilisateur_suiveur: int, id_utilisateur_suivi: int, user = Depends(get_current_user)):
    """S'abonner à un utilisateur par l'utilisateur connecté."""
    
    AbonnementService().creer_abonnement(id_utilisateur_suiveur, id_utilisateur_suivi)
    return {"message": "Abonnement créé"}

@app.delete("/abonnements")
def supprimer_abonnement(id_utilisateur_suiveur: int, id_utilisateur_suivi: int, user = Depends(get_current_user)):
    """Se désabonner d'un utilisateur par l'utilisateur connecté."""
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

@app.get("/statistiques/total/{id_utilisateur}")
def statistiques_totales(id_utilisateur: int, user = Depends(get_current_user)):
    """Récupérer les statistiques globales (totales) d'un utilisateur."""
    
    service = ServiceStatistiques()
    
    # Récupérer les données nécessaires via les méthodes de ServiceStatistiques
    nombre_activites = service.calculer_nombre_activites_total(id_utilisateur)
    distance_totale = service.calculer_distance_totale(id_utilisateur)
    duree_totale = service.calculer_duree_totale(id_utilisateur)
    
    return {
        "nombre_activites_total": nombre_activites,
        "distance_totale": distance_totale,
        "duree_totale": duree_totale
    }

@app.get("/statistiques/semaine/{id_utilisateur}")
def statistiques_semaine(id_utilisateur: int, date_reference: str, user = Depends(get_current_user)):
    """Récupérer les statistiques d'une semaine spécifique d'un utilisateur."""
    
    service = ServiceStatistiques()
    
    # Récupérer les données de la semaine demandée via les méthodes de ServiceStatistiques
    nombre_activites_semaine = service.calculer_nombre_activites_semaine(id_utilisateur, date_reference)
    distance_semaine = service.calculer_distance_semaine(id_utilisateur, date_reference)
    duree_semaine = service.calculer_duree_semaine(id_utilisateur, date_reference)
    
    return {
        "nombre_activites_semaine": nombre_activites_semaine,
        "distance_semaine": distance_semaine,
        "duree_semaine": duree_semaine
    }


# --- Endpoint Upload GPX ---
@app.post("/upload-gpx")
async def upload_gpx(file: UploadFile = File(...)):
    """Upload et parsing d'un fichier GPX."""
    content = await file.read()
    try:
        parsed_activite = parse_gpx(content)
    except Exception as e:
        logging.error(f"Erreur lors du parsing du fichier GPX : {e}")
        return {"message": "Erreur lors du parsing du fichier GPX"}
    return {"message": "Fichier GPX analysé", "activite": parsed_activite}


# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9876)

    logging.info("Arret du Webservice")
