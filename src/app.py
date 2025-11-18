from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from fastapi import FastAPI, UploadFile, File, HTTPException
import io

import logging
from utils.log_init import initialiser_logs

from service.activite_service import ActiviteService
from service.utilisateur_service import UtilisateurService
from service.abonnement_service import AbonnementService
from service.service_statistiques import ServiceStatistiques
from service.fil_dactualite_service import Fildactualite

from utils.gpx_parser import parse_gpx
from utils.verifier_date import verifier_date

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
    utilisateur = UtilisateurService().trouver_par_id(id_utilisateur)
    if not utilisateur:
        return {"message": "Cet utilisateur n'existe pas"}
    liste_activites = ActiviteService().lister_activites(id_utilisateur)
    if liste_activites:
        return liste_activites
    else:
        return {"message": "Erreur"}

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
    activite_creee = ActiviteService().creer_activite(user["id_utilisateur"], sport, date_activite, distance, duree)
    if not activite_creee:
        raise HTTPException(status_code=400, detail="Erreur lors de la création de l'activité")
    return {"message": "Activité créée", "activite": activite_creee}

@app.put("/activites/{id_activite}")
def modifier_activite(id_activite: int, sport: str, user = Depends(get_current_user)):
    """Modifier une activité existante appartenant à l'utilisateur connecté."""
    activite = ActiviteService().trouver_activite_par_id(id_activite)
    if not activite:
        return {"message": "Cette activité n'existe pas"}
    if not activite.id_utilisateur == user["id_utilisateur"]:
        return {"message": "Cette activité ne vous appartient pas"}
    activite_modifie = ActiviteService().modifier_activite(id_activite, sport)
    if not activite_modifie:
        raise HTTPException(status_code=400, detail="Erreur lors de la modification de l'activité")
    return {"message": "Activité modifiée", "activite": updated_activite}

@app.delete("/activites/{id_activite}")
def supprimer_activite(id_activite: int, user = Depends(get_current_user)):
    """Supprimer une activité appartenant à l'utilisateur connecté."""
    activite = ActiviteService().trouver_activite_par_id(id_activite)
    if not activite:
        return {"message": "Cette activité n'existe pas"}
    if not activite.id_utilisateur == user["id_utilisateur"]:
        return {"message": "Cette activité ne vous appartient pas"}
    supprime = ActiviteService().supprimer_activite(id_activite)
    if not supprime:
        raise HTTPException(status_code=400, detail="Erreur lors de la suppression de l'activité")
    return {"message": "Activité supprimée"}


# --- Endpoints Interactions avec les activités ---

@app.post("/jaimes")
def ajouter_jaime(id_activite: int, user = Depends(get_current_user)):
    """Ajouter un jaime à une activité pour l'utilisateur connecté."""
    activite = ActiviteService().trouver_activite_par_id(id_activite)
    if not activite:
        return {"message": "Cette activité n'existe pas"}
    jaime_cree = ActiviteService().ajouter_jaime(user["id_utilisateur"], id_activite)
    if not jaime_cree:
        raise HTTPException(status_code=400, detail="Erreur lors de l'ajout du jaime")
    return {"message": "Jaime ajouté", "jaime": jaime_cree}

@app.delete("/jaimes/{id_activite}/{id_utilisateur}")
def supprimer_jaime(id_activite: int, user = Depends(get_current_user)):
    """Supprimer le jaime appartenant à l'utilisateur connecté d'une activité."""
    activite = ActiviteService().trouver_activite_par_id(id_activite)
    if not activite:
        return {"message": "Cette activité n'existe pas"}
    jaime = ActiviteService().jaime_existe(id_activite, user["id_utilisateur"])
    if not jaime:
        return {"message": "Ce jaime n'existe pas"}
    supprime = ActiviteService().supprimer_jaime(id_activite, user["id_utilisateur"])
    if not supprime:
        raise HTTPException(status_code=400, detail="Erreur lors de la suppression du jaime")
    return {"message": "Jaime supprimé"}

@app.post("/commentaires")
def ajouter_commentaire(id_activite: int, commentaire: str, user = Depends(get_current_user)):
    """Ajouter un commentaire à une activité pour l'utilisateur connecté."""
    activite = ActiviteService().trouver_activite_par_id(id_activite)
    if not activite:
        return {"message": "Cette activité n'existe pas"}
    commentaire_cree = ActiviteService().ajouter_commentaire(user["id_utilisateur"], id_activite, commentaire)
    if not commentaire_cree:
        raise HTTPException(status_code=400, detail="Erreur lors de la création du commentaire")
    return {"message": "Commentaire ajouté", "commentaire": commentaire_cree}

@app.delete("/commentaires/{id_commentaire}")
def supprimer_commentaire(id_commentaire: int, user = Depends(get_current_user)):
    """Supprimer un commentaire appartenant à l'utilisateur connecté."""
    commentaire = ActiviteService().trouver_commentaire_par_id(id_commentaire)
    if not commentaire:
        return {"message": "Ce commentaire n'existe pas"}
    if not commentaire.id_auteur == user["id_utilisateur"]:
        return {"message": "Ce commentaire ne vous appartient pas"}
    supprime = ActiviteService().supprimer_commentaire(id_commentaire)
    if not supprime:
        raise HTTPException(status_code=400, detail="Erreur lors de la suppression du commentaire")
    return {"message": "Commentaire supprimé"}


# --- Endpoints Abonnements ---

@app.post("/abonnements")
def creer_abonnement(id_utilisateur_suivi: int, user = Depends(get_current_user)):
    """S'abonner à un utilisateur par l'utilisateur connecté."""
    utilisateur_suivi = UtilisateurService().trouver_par_id(id_utilisateur_suivi)
    if not utilisateur_suivi:
        return {"message": "Cet utilisateur n'existe pas"}
    id_utilisateur_suiveur = user["id_utilisateur"]
    abonnement_cree = AbonnementService().creer_abonnement(id_utilisateur_suiveur, id_utilisateur_suivi)
    if not abonnement_cree:
        raise HTTPException(status_code=400, detail="Erreur lors de la création de l'abonnement")
    return {"message": "Abonnement créé", "abonnement": abonnement_cree}

@app.delete("/abonnements")
def supprimer_abonnement(id_utilisateur_suivi: int, user = Depends(get_current_user)):
    """Se désabonner d'un utilisateur par l'utilisateur connecté."""
    utilisateur_suivi = UtilisateurService().trouver_par_id(id_utilisateur_suivi)
    if not utilisateur_suivi:
        return {"message": "Cet utilisateur n'existe pas"}
    id_utilisateur_suiveur = user["id_utilisateur"]
    abonnement = ActiviteService().abonnement_existe(id_utilisateur_suiveur, id_utilisateur_suivi)
    if not abonnement:
        return {"message": "Cet abonnement n'existe pas"}
    supprime = AbonnementService().supprimer_abonnement(id_utilisateur_suiveur, id_utilisateur_suivi)
    if not supprime:
        raise HTTPException(status_code=400, detail="Erreur lors de la suppression de l'abonnement")
    return {"message": "Abonnement supprimé"}

@app.get("/abonnements/suivis/{id_utilisateur}")
def lister_abonnements_suivis(id_utilisateur: int, user = Depends(get_current_user)):
    """Lister les utilisateurs suivis par l'utilisateur donné."""
    utilisateur_suiveur = UtilisateurService().trouver_par_id(id_utilisateur)
    if not utilisateur_suiveur:
        return {"message": "Cet utilisateur n'existe pas"}
    suivis = AbonnementService().lister_utilisateurs_suivis(id_utilisateur)
    if suivis:
        return suivis
    else:
        return {"message": "Erreur"}

@app.get("/abonnements/suiveurs/{id_utilisateur}")
def lister_abonnements_suiveurs(id_utilisateur: int, user = Depends(get_current_user)):
    """Lister les utilisateurs qui suivent l'utilisateur."""
    utilisateur_suivi = UtilisateurService().trouver_par_id(id_utilisateur)
    if not utilisateur_suivi:
        return {"message": "Cet utilisateur n'existe pas"}
    suiveurs = AbonnementService().lister_utilisateurs_suiveurs(id_utilisateur)
    if suiveurs:
        return suiveurs
    else:
        return {"message": "Erreur"}


# --- Endpoints Fil d'actualité ---

@app.get("/fil-dactualite/{id_utilisateur}")
def fil_dactualite(id_utilisateur: int, user = Depends(get_current_user)):
    """Afficher le fil d'actualités de l'utilisateur."""
    fil_dactualite = Fildactualite().creer_fil_dactualite(id_utilisateur)
    if fil_dactualite:
        return fil_dactualite
    else:
        return {"message": "Erreur"}


# --- Endpoints Statistiques ---

@app.get("/statistiques/total/{id_utilisateur}")
def statistiques_totales(id_utilisateur: int, user = Depends(get_current_user)):
    """Récupérer les statistiques globales (totales) d'un utilisateur."""
    
    utilisateur = UtilisateurService().trouver_par_id(id_utilisateur)
    if not utilisateur:
        return {"message": "Cet utilisateur n'existe pas"}
    
    # Récupérer les données nécessaires via les méthodes de ServiceStatistiques
    nombre_activites = ServiceStatistiques().calculer_nombre_activites_total(id_utilisateur)
    distance_totale = ServiceStatistiques().calculer_distance_totale(id_utilisateur)
    duree_totale = ServiceStatistiques().calculer_duree_totale(id_utilisateur)

    if all(x is not None for x in [nombre_activites, distance_totale, duree_totale]):
        return {
            "nombre_activites_total": nombre_activites,
            "distance_totale": distance_totale,
            "duree_totale": duree_totale
        }  
    else:
        return {"message": "Erreur"}

@app.get("/statistiques/semaine/{id_utilisateur}")
def statistiques_semaine(id_utilisateur: int, date_reference: str, user = Depends(get_current_user)):
    """Récupérer les statistiques d'une semaine spécifique d'un utilisateur."""
    
    utilisateur = UtilisateurService().trouver_par_id(id_utilisateur)
    if not utilisateur:
        return {"message": "Cet utilisateur n'existe pas"}
    
    if not verifier_date(date_reference):
        return {"message": f"Le format de la date est incorrect. Utilisez le format YYYY-MM-DD."}
    
    # Récupérer les données de la semaine demandée via les méthodes de ServiceStatistiques
    nombre_activites_semaine = ServiceStatistiques().calculer_nombre_activites_semaine(id_utilisateur, date_reference)
    distance_semaine = ServiceStatistiques().calculer_distance_semaine(id_utilisateur, date_reference)
    duree_semaine = ServiceStatistiques().calculer_duree_semaine(id_utilisateur, date_reference)
    
    if all(x is not None for x in [nombre_activites_semaine, distance_semaine, duree_semaine]):
        return {
            "nombre_activites_semaine": nombre_activites_semaine,
            "distance_semaine": distance_semaine,
            "duree_semaine": duree_semaine
        }
    else:
        return {"message": "Erreur"}


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
