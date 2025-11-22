from typing import List
from datetime import datetime

from utils.log_decorator import log

from business_object.activite import Activite
from business_object.commentaire import Commentaire
from business_object.jaime import Jaime

from dao.utilisateur_dao import UtilisateurDao
from dao.activite_dao import ActiviteDao
from dao.commentaire_dao import CommentaireDao
from dao.jaime_dao import JaimeDao

from utils.utils_date import verifier_date

from exceptions import NotFoundError, AlreadyExistsError

class ActiviteService:
    """Classe contenant les méthodes de service des activités Utilisateurs"""

    # --- Activités ---
    
    @log
    def creer_activite(self, id_utilisateur: int, sport: str, date_activite: str, distance: float, duree: float) -> bool:
        """Crée une nouvelle activité (distance en km, durée en minutes)"""
        if not UtilisateurDao().verifier_id_existant(id_utilisateur):
            raise NotFoundError(f"L'utilisateur avec l'id {id_utilisateur} n'existe pas")
        if not verifier_date(date_activite):
            raise ValueError(f"Le format de la date {date_activite} est incorrect. Utilisez le format YYYY-MM-DD.")
        
        activite = Activite(
            id_utilisateur=id_utilisateur,
            sport=sport,
            date_activite=date_activite,
            distance=distance,
            duree=duree
        )
        return ActiviteDao().creer(activite) # Appel à DAO pour l'enregistrement

    @log
    def supprimer_activite(self, id_activite: int) -> bool:
        """Supprime une activité existante"""
        if not ActiviteDao().verifier_id_existant(id_activite):
            raise NotFoundError("Cette activité n'existe pas")
        
        return ActiviteDao().supprimer(id_activite)

    @log
    def modifier_activite(self, id_activite: int, sport: str) -> bool:
        """Modifie une activité existante"""
        if not ActiviteDao().verifier_id_existant(id_activite):
            raise NotFoundError("Cette activité n'existe pas")
        
        activite = ActiviteDao().trouver_par_id(id_activite=id_activite)  # Récupère l'activité par son ID

        nouveau_activite = Activite(
            id_utilisateur=activite.id_utilisateur,
            sport=sport, # Modification du sport de l'activité
            date_activite=activite.date_activite,
            distance=activite.distance,
            duree=activite.duree
        )

        return ActiviteDao().modifier(nouveau_activite) # Appel à DAO pour modification dans la base de données
    
    @log
    def trouver_activite_par_id(self, id_activite: int):
        """Trouver une activité par son id"""
        if not ActiviteDao().verifier_id_existant(id_activite):
            raise NotFoundError("Cette activité n'existe pas")
        
        return ActiviteDao().trouver_par_id(id_activite=id_activite)

    @log
    def lister_activites(self, id_utilisateur: int) -> List[Activite]:
        """Liste toutes les activités d'un utilisateur donné"""
        if not UtilisateurDao().verifier_id_existant(id_utilisateur):
            raise NotFoundError("Cet utilisateur n'existe pas")
        
        return ActiviteDao().lister_par_utilisateur(id_utilisateur=id_utilisateur)

    @log
    def lister_activites_filtres(self, id_utilisateur: int, sport: str = None, date_debut: str = None, date_fin: str = None) -> List[Activite]:
        """Liste les activités d'un utilisateur avec des filtres optionnels (sport, date_debut, date_fin)"""
        if not UtilisateurDao().verifier_id_existant(id_utilisateur):
            raise NotFoundError("Cet utilisateur n'existe pas")
        if date_debut is not None and not verifier_date(date_debut):
            raise ValueError(f"Le format de la date {date_debut} est incorrect. Utilisez le format YYYY-MM-DD.")
        if date_fin is not None and not verifier_date(date_fin):
            raise ValueError(f"Le format de la date {date_fin} est incorrect. Utilisez le format YYYY-MM-DD.")
        if sport is not None:
            sport = Activite.valider_sport(sport)
        
        return ActiviteDao().lister_activites_filtres(id_utilisateur=id_utilisateur, sport=sport, date_debut=date_debut, date_fin=date_fin)


    # --- Jaimes ---

    @log
    def ajouter_jaime(self, id_activite: int, id_utilisateur: int) -> Jaime:
        """Ajoute un "j'aime" à une activité"""
        if not ActiviteDao().verifier_id_existant(id_activite):
            raise NotFoundError("Cette activité n'existe pas")
        if not UtilisateurDao().verifier_id_existant(id_utilisateur):
            raise NotFoundError("Cet utilisateur n'existe pas")
        if JaimeDao().existe(id_activite, id_utilisateur):
            raise AlreadyExistsError("Ce jaime existe déjà")
        
        jaime = Jaime(id_activite=id_activite, id_auteur=id_utilisateur)
        return JaimeDao().creer(jaime)

    @log
    def supprimer_jaime(self, id_activite: int, id_utilisateur: int) -> bool:
        """Supprime un "j'aime" d'une activité"""
        if not ActiviteDao().verifier_id_existant(id_activite):
            raise NotFoundError("Cette activité n'existe pas")
        if not UtilisateurDao().verifier_id_existant(id_utilisateur):
            raise NotFoundError("Cet utilisateur n'existe pas")
        if not JaimeDao().existe(id_activite, id_utilisateur):
            raise NotFoundError("Ce jaime n'existe pas")

        return JaimeDao().supprimer(id_activite, id_utilisateur)
    
    @log
    def jaime_existe(self, id_activite: int, id_utilisateur: int) -> bool:
        """Vérifier si un jaime existe dans la base de données"""
        if not ActiviteDao().verifier_id_existant(id_activite):
            raise NotFoundError("Cette activité n'existe pas")
        if not UtilisateurDao().verifier_id_existant(id_utilisateur):
            raise NotFoundError("Cet utilisateur n'existe pas")
        
        return JaimeDao().existe(id_activite, id_utilisateur)
    
    @log
    def compter_jaimes_par_activite(self, id_activite: int) -> int:
        """Compte le nombre de jaimes pour une activité donnée."""
        if not ActiviteDao().verifier_id_existant(id_activite):
            raise NotFoundError("Cette activité n'existe pas")
        
        return JaimeDao().compter_par_activite(id_activite)


    # --- Commentaires ---

    @log
    def ajouter_commentaire(self, id_activite: int, id_utilisateur: int, contenu: str) -> Commentaire:
        """Ajoute un commentaire à une activité"""
        if not ActiviteDao().verifier_id_existant(id_activite):
            raise NotFoundError("Cette activité n'existe pas")
        if not UtilisateurDao().verifier_id_existant(id_utilisateur):
            raise NotFoundError("Cet utilisateur n'existe pas")
        
        commentaire = Commentaire(
            id_activite=id_activite,
            id_auteur=id_utilisateur,
            contenu=contenu,
            date_commentaire=datetime.now()
        )
        return CommentaireDao().creer(commentaire)

    @log
    def supprimer_commentaire(self, id_commentaire: int) -> bool:
        """Supprime un commentaire d'une activité"""
        commentaire = CommentaireDao().trouver_par_id(id_commentaire)
        if not commentaire:
            raise NotFoundError("Ce commentaire n'existe pas")

        return CommentaireDao().supprimer(id_commentaire)

    @log
    def lister_commentaires(self, id_activite: int) -> List[Commentaire]:
        """Lister tous les commentaires d'une activité"""
        if not ActiviteDao().verifier_id_existant(id_activite):
            raise NotFoundError("Cette activité n'existe pas")
        
        return CommentaireDao().lister_par_activite(id_activite=id_activite)
    
    @log
    def trouver_commentaire_par_id(self, id_commentaire: int) -> Commentaire:
        """Trouver un commentaire par son id"""
        commentaire = CommentaireDao().trouver_par_id(id_commentaire)
        if not commentaire:
            raise NotFoundError("Ce commentaire n'existe pas")
        
        return commentaire
