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

@app.post("/inscription")
def inscription(
    pseudo: str,
    mot_de_passe: str,
    nom: str,
    prenom: str,
    date_de_naissance: str,
    sexe: str,
):
    """Créer un nouveau compte utilisateur.
    La date de naissance doit être au format YYYY-MM-DD"""
    succes = UtilisateurService().inscrire(
        pseudo=pseudo,
        mot_de_passe=mot_de_passe,
        nom=nom,
        prenom=prenom,
        date_de_naissance=date_de_naissance,
        sexe=sexe,
    )

    if not succes:
        raise HTTPException(
            status_code=400,
            detail="Impossible d'inscrire l'utilisateur (pseudo peut-être déjà utilisé)",
        )

    return {"message": "Utilisateur inscrit avec succès"}


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
    if liste_activites is None:
        raise HTTPException(status_code=400, detail="Erreur lors de la récupération des activités de l'utilisateur")
    return liste_activites

@app.get("/activites-filtres/{id_utilisateur}")
def activites_par_utilisateur_filtres(
    id_utilisateur: int,
    sport: str = None,
    date_debut: str = None,
    date_fin: str = None,
    user = Depends(get_current_user),
):
    """Lister les activités d'un utilisateur avec filtres facultatifs."""
    utilisateur = UtilisateurService().trouver_par_id(id_utilisateur)
    if not utilisateur:
        return {"message": "Cet utilisateur n'existe pas"}

    try:
        liste_activites = ActiviteService().lister_activites_filtres(
            id_utilisateur=id_utilisateur,
            sport=sport,
            date_debut=date_debut,
            date_fin=date_fin,
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erreur lors de la récupération des activités filtrées : {e}",
        )

    if liste_activites is None:
        raise HTTPException(
            status_code=400,
            detail="Erreur lors de la récupération des activités de l'utilisateur",
        )

    return liste_activites

@app.post("/activites")
async def creer_activite(file: UploadFile = File(...), sport: str = "randonnée", user = Depends(get_current_user)):
    """Créer une nouvelle activité avec un fichier GPX pour l'utilisateur connecté."""
    content = await file.read()
    try:
        parsed_activite = parse_gpx(content)
    except Exception as e:
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


# --- Endpoints Utilisateurs ---

@app.get("/utilisateurs/{id_utilisateur}")
def consulter_utilisateur_par_id(id_utilisateur: int, user = Depends(get_current_user)):
    """Récupérer un utilisateur grâce à son ID."""
    utilisateur = UtilisateurService().trouver_par_id(id_utilisateur)
    if not utilisateur:
        raise HTTPException(status_code=400, detail="Cet utilisateur n'existe pas")
    return utilisateur

@app.get("/utilisateurs/pseudo/{pseudo}")
def consulter_utilisateur_par_pseudo(pseudo: str, user = Depends(get_current_user)):
    """Récupérer un utilisateur grâce à son pseudo."""
    utilisateur = UtilisateurService().trouver_par_pseudo(pseudo)
    if not utilisateur:
        raise HTTPException(status_code=400, detail="Cet utilisateur n'existe pas")
    return utilisateur

@app.get("/utilisateurs")
def lister_utilisateurs(user = Depends(get_current_user)):
    """Lister tous les utilisateurs."""
    utilisateurs = UtilisateurService().lister_utilisateurs()
    if utilisateurs is None:
        raise HTTPException(status_code=400, detail="Erreur lors de la récupération des utilisateurs")
    return utilisateurs
        

# --- Endpoints Jaimes ---

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

@app.get("/jaimes/existe")
def jaime_existe(id_activite: int, id_auteur: int, user = Depends(get_current_user)):
    """Vérifier si un jaime existe pour une activité et un auteur donné."""
    utilisateur = UtilisateurService().trouver_par_id(id_auteur)
    if not utilisateur:
        raise HTTPException(status_code=400, detail="Cet utilisateur n'existe pas")
    activite = ActiviteService().trouver_activite_par_id(id_activite)
    if not activite:
        raise HTTPException(status_code=400, detail="Cette activité n'existe pas")

    existe = ActiviteService().jaime_existe(id_activite, id_auteur)
    return existe


# --- Endpoints Commentaires ---

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

@app.get("/commentaires/{id_activite}")
def lister_commentaires(id_activite: int, user = Depends(get_current_user)):
    """Lister les commentaires d'une activité donnée."""
    activite = ActiviteService().trouver_activite_par_id(id_activite)
    if not activite:
        raise HTTPException(status_code=400, detail="Cette activité n'existe pas")

    commentaires = ActiviteService().lister_commentaires(id_activite)
    if commentaires is None:
        raise HTTPException(status_code=400, detail="Erreur lors de la récupération des commentaires")

    return commentaires

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

@app.get("/abonnements/existe")
def abonnement_existe(id_utilisateur_suiveur: int, id_utilisateur_suivi: int, user = Depends(get_current_user)):
    """Vérifier si un abonnement existe entre deux utilisateurs."""
    utilisateur_suiveur = UtilisateurService().trouver_par_id(id_utilisateur_suiveur)
    utilisateur_suivi = UtilisateurService().trouver_par_id(id_utilisateur_suivi)

    if not utilisateur_suiveur or not utilisateur_suivi:
        raise HTTPException(status_code=400, detail="L'un des utilisateurs n'existe pas")

    existe = ActiviteService().abonnement_existe(id_utilisateur_suiveur, id_utilisateur_suivi)
    return existe

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
        return {"message": "Erreur lors du parsing du fichier GPX"}
    return {"message": "Fichier GPX analysé", "activite": parsed_activite}


# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9876)

    logging.info("Arret du Webservice")
