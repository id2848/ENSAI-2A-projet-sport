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
from service.statistiques_service import StatistiquesService
from service.fil_dactualite_service import Fildactualite

from utils.gpx_parser import parse_gpx
from utils.utils_date import verifier_date

from exceptions import NotFoundError, AlreadyExistsError, InvalidPasswordError

# --- Configuration ---

app = FastAPI(title="Webservice Sports ENSAI")

initialiser_logs("Webservice")

# Authentification basique

security = HTTPBasic()

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password

    try:
        return UtilisateurService().se_connecter(username, password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Authentification : " + str(e))
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail="Authentification : " + str(e))
    except InvalidPasswordError as e:
        raise HTTPException(status_code=401, detail="Authentification : " + str(e))

# ----------------------------------------------------------

# --- Endpoints Authentification ---

@app.get("/me", tags=["Authentification"])
def me(user = Depends(get_current_user)):
    """Se connecter ou consulter son profil utilisateur"""
    return user

@app.get("/logout", tags=["Authentification"])
async def logout():
    """Se déconnecter de son compte utilisateur"""
    return HTMLResponse(content="Vous vous êtes déconnecté", status_code=status.HTTP_401_UNAUTHORIZED)

@app.post("/inscription", tags=["Authentification"])
def inscription(
    pseudo: str,
    mot_de_passe: str,
    nom: str,
    prenom: str,
    date_de_naissance: str,
    sexe: str,
):
    """Créer un nouveau compte utilisateur.
    La date de naissance doit être au format YYYY-MM-DD
    """
    try:
        UtilisateurService().inscrire(
            pseudo=pseudo,
            mot_de_passe=mot_de_passe,
            nom=nom,
            prenom=prenom,
            date_de_naissance=date_de_naissance,
            sexe=sexe,
        )
        return {"message": "Utilisateur inscrit avec succès"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except AlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))


# --- Endpoints de base ---

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirige vers la documentation de l'API."""
    return RedirectResponse(url="/docs")


# --- Endpoints Gestion des activités ---

@app.post("/activites", tags=["Activité"])
async def creer_activite(file: UploadFile = File(...), sport: str = "randonnée", user = Depends(get_current_user)):
    """Créer une nouvelle activité avec un fichier GPX pour l'utilisateur connecté."""
    # Parsing GPX
    content = await file.read()
    try:
        parsed_activite = parse_gpx(content)
        date_activite = parsed_activite["date"]
        distance = parsed_activite["distance totale"]
        duree = parsed_activite["durée totale"]
    except Exception as e:
        raise HTTPException(status_code=400, detail="Erreur lors du parsing du fichier GPX")

    # Création Activité
    try:
        activite_creee = ActiviteService().creer_activite(user["id_utilisateur"], sport, date_activite, distance, duree)
        return {"message": "Activité créée", "activite": activite_creee}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/activites/{id_activite}", tags=["Activité"])
def modifier_activite(id_activite: int, sport: str, user = Depends(get_current_user)):
    """Modifier une activité existante appartenant à l'utilisateur connecté."""
    # Vérification appartenance
    try:
        activite = ActiviteService().trouver_activite_par_id(id_activite)
        if activite.id_utilisateur != user["id_utilisateur"]:
            raise HTTPException(status_code=403, detail="Cette activité ne vous appartient pas")
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    try:
        activite_modifie = ActiviteService().modifier_activite(id_activite, sport)
        return {"message": "Activité modifiée", "activite": activite_modifie}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/activites/{id_activite}", tags=["Activité"])
def supprimer_activite(id_activite: int, user = Depends(get_current_user)):
    """Supprimer une activité appartenant à l'utilisateur connecté."""
    # Vérification appartenance
    try:
        activite = ActiviteService().trouver_activite_par_id(id_activite)
        if activite.id_utilisateur != user["id_utilisateur"]:
            raise HTTPException(status_code=403, detail="Cette activité ne vous appartient pas")
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    try:
        supprime = ActiviteService().supprimer_activite(id_activite)
        return {"message": "Activité supprimée avec succès"}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/activites/{id_utilisateur}", tags=["Activité"])
def activites_par_utilisateur(id_utilisateur: int, user = Depends(get_current_user)):
    """Lister les activités d'un utilisateur donné."""
    try:
        return ActiviteService().lister_activites(id_utilisateur)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/activites-filtres/{id_utilisateur}", tags=["Activité"])
def activites_par_utilisateur_filtres(
    id_utilisateur: int,
    sport: str = None,
    date_debut: str = None,
    date_fin: str = None,
    user = Depends(get_current_user),
):
    """Lister les activités d'un utilisateur avec filtres facultatifs.
    Les dates doivent être au format YYYY-MM-DD"""
    try:
        liste_activites = ActiviteService().lister_activites_filtres(
            id_utilisateur=id_utilisateur,
            sport=sport,
            date_debut=date_debut,
            date_fin=date_fin,
        )
        return liste_activites
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- Endpoints Utilisateurs ---

@app.get("/utilisateurs/{id_utilisateur}", tags=["Utilisateur"])
def consulter_utilisateur_par_id(id_utilisateur: int, user = Depends(get_current_user)):
    """Récupérer un utilisateur grâce à son ID."""
    try:
        return UtilisateurService().trouver_par_id(id_utilisateur)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/utilisateurs/pseudo/{pseudo}", tags=["Utilisateur"])
def consulter_utilisateur_par_pseudo(pseudo: str, user = Depends(get_current_user)):
    """Récupérer un utilisateur grâce à son pseudo."""
    try:
        return UtilisateurService().trouver_par_pseudo(pseudo)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/utilisateurs", tags=["Utilisateur"])
def lister_utilisateurs(user = Depends(get_current_user)):
    """Lister tous les utilisateurs."""
    return UtilisateurService().lister_utilisateurs() # pas de paramètres donc pas d'erreur côté client


# --- Endpoints Jaimes ---

@app.post("/jaimes", tags=["Jaime"])
def ajouter_jaime(id_activite: int, user = Depends(get_current_user)):
    """Ajouter un jaime à une activité pour l'utilisateur connecté."""
    try:
        id_auteur = user["id_utilisateur"]
        return ActiviteService().ajouter_jaime(id_activite, id_auteur)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))

@app.delete("/jaimes/{id_activite}", tags=["Jaime"])
def supprimer_jaime(id_activite: int, user = Depends(get_current_user)):
    """Supprimer le jaime appartenant à l'utilisateur connecté d'une activité.""" 
    try:
        ActiviteService().supprimer_jaime(id_activite, user["id_utilisateur"])
        return {"message": "Jaime supprimé avec succès"}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/jaimes/existe", tags=["Jaime"])
def jaime_existe(id_activite: int, id_auteur: int, user = Depends(get_current_user)):
    """Vérifier si un jaime existe pour une activité et un auteur donné."""
    try:
        return ActiviteService().jaime_existe(id_activite, id_auteur)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/jaimes/compter", tags=["Jaime"])
def compter_jaimes(id_activite: int, user = Depends(get_current_user)):
    """Compter le nombre de jaimes pour une activité donnée."""

    try:
        nombre_jaimes = ActiviteService().compter_jaimes_par_activite(id_activite)
        return {"id_activite": id_activite, "nombre_jaimes": nombre_jaimes}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


# --- Endpoints Commentaires ---

@app.post("/commentaires", tags=["Commentaire"])
def ajouter_commentaire(id_activite: int, commentaire: str, user = Depends(get_current_user)):
    """Ajouter un commentaire à une activité pour l'utilisateur connecté."""
    try:
        id_utilisateur = user["id_utilisateur"]
        return ActiviteService().ajouter_commentaire(id_activite, id_utilisateur, commentaire)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/commentaires/{id_commentaire}", tags=["Commentaire"])
def supprimer_commentaire(id_commentaire: int, user = Depends(get_current_user)):
    """Supprimer un commentaire appartenant à l'utilisateur connecté."""
    # Vérification appartenance
    try:
        commentaire = ActiviteService().trouver_commentaire_par_id(id_commentaire)
        if commentaire.id_auteur != user["id_utilisateur"]:
            raise HTTPException(status_code=403, detail="Ce commentaire ne vous appartient pas")
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    try:
        ActiviteService().supprimer_commentaire(id_commentaire)
        return {"message": "Commentaire supprimé avec succès"}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/commentaires/{id_activite}", tags=["Commentaire"])
def lister_commentaires(id_activite: int, user = Depends(get_current_user)):
    """Lister les commentaires d'une activité donnée."""
    try:
        return ActiviteService().lister_commentaires(id_activite)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


# --- Endpoints Abonnements ---

@app.post("/abonnements", tags=["Abonnement"])
def creer_abonnement(id_utilisateur_suivi: int, user = Depends(get_current_user)):
    """S'abonner à un utilisateur par l'utilisateur connecté."""
    try:
        id_utilisateur_suiveur = user["id_utilisateur"]
        return AbonnementService().creer_abonnement(id_utilisateur_suiveur, id_utilisateur_suivi)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))

@app.delete("/abonnements", tags=["Abonnement"])
def supprimer_abonnement(id_utilisateur_suivi: int, user = Depends(get_current_user)):
    """Se désabonner d'un utilisateur par l'utilisateur connecté."""
    try:
        id_utilisateur_suiveur = user["id_utilisateur"]
        AbonnementService().supprimer_abonnement(id_utilisateur_suiveur, id_utilisateur_suivi)
        return {"message": "Abonnement supprimé avec succès"}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/abonnements/existe", tags=["Abonnement"])
def abonnement_existe(id_utilisateur_suiveur: int, id_utilisateur_suivi: int, user = Depends(get_current_user)):
    """Vérifier si un abonnement existe entre deux utilisateurs."""
    try:
        return AbonnementService().abonnement_existe(id_utilisateur_suiveur, id_utilisateur_suivi)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/abonnements/suivis/{id_utilisateur}", tags=["Abonnement"])
def lister_abonnements_suivis(id_utilisateur: int, user = Depends(get_current_user)):
    """Lister les utilisateurs suivis par l'utilisateur donné."""
    try:
        return AbonnementService().lister_utilisateurs_suivis(id_utilisateur)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/abonnements/suiveurs/{id_utilisateur}", tags=["Abonnement"])
def lister_abonnements_suiveurs(id_utilisateur: int, user = Depends(get_current_user)):
    """Lister les utilisateurs qui suivent l'utilisateur."""
    try:
        return AbonnementService().lister_utilisateurs_suiveurs(id_utilisateur)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


# --- Endpoints Fil d'actualité ---

@app.get("/fil-dactualite/{id_utilisateur}", tags=["Fil d'actualité"])
def fil_dactualite(id_utilisateur: int, user = Depends(get_current_user)):
    """Afficher le fil d'actualités de l'utilisateur."""
    try:
        return Fildactualite().creer_fil_dactualite(id_utilisateur)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


# --- Endpoints Statistiques ---

@app.get("/statistiques/total/{id_utilisateur}", tags=["Statistiques"])
def statistiques_totales(id_utilisateur: int, user = Depends(get_current_user)):
    """Récupérer les statistiques globales (totales) d'un utilisateur."""
    try:
        # Récupérer les données nécessaires via les méthodes de StatistiquesService
        nombre_activites = StatistiquesService().calculer_nombre_activites_total(id_utilisateur)
        distance_totale = StatistiquesService().calculer_distance_totale(id_utilisateur)
        duree_totale = StatistiquesService().calculer_duree_totale(id_utilisateur)
        return {
            "nombre_activites_total": nombre_activites,
            "distance_totale": distance_totale,
            "duree_totale": duree_totale
        }
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/statistiques/semaine/{id_utilisateur}", tags=["Statistiques"])
def statistiques_semaine(id_utilisateur: int, date_reference: str, user = Depends(get_current_user)):
    """Récupérer les statistiques d'une semaine spécifique d'un utilisateur.
    La date doit être au format YYYY-MM-DD"""
    try:
        # Récupérer les données de la semaine demandée via les méthodes de StatistiquesService
        nombre_activites_semaine = StatistiquesService().calculer_nombre_activites_semaine(id_utilisateur, date_reference)
        distance_semaine = StatistiquesService().calculer_distance_semaine(id_utilisateur, date_reference)
        duree_semaine = StatistiquesService().calculer_duree_semaine(id_utilisateur, date_reference)
        return {
            "nombre_activites_semaine": nombre_activites_semaine,
            "distance_semaine": distance_semaine,
            "duree_semaine": duree_semaine
        }
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- Endpoint Upload GPX ---
@app.post("/upload-gpx", tags=["Utilitaires"])
async def upload_gpx(file: UploadFile = File(...)):
    """Upload et parsing d'un fichier GPX."""
    content = await file.read()
    try:
        parsed_activite = parse_gpx(content)
    except Exception as e:
        return {"message": "Erreur lors du parsing du fichier GPX"}
    return {"message": "Fichier GPX analysé", "activite": parsed_activite}


# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9876)

    logging.info("Arret du Webservice")
