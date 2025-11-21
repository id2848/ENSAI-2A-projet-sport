from utils.log_decorator import log

from dao.abonnement_dao import AbonnementDao
from dao.activite_dao import ActiviteDao
from dao.commentaire_dao import CommentaireDao
from dao.jaime_dao import JaimeDao
from dao.utilisateur_dao import UtilisateurDao

from service.abonnement_service import AbonnementService

from business_object.abonnement import Abonnement
from business_object.activite import Activite
from business_object.commentaire import Commentaire
from business_object.jaime import Jaime
from business_object.utilisateur import Utilisateur

from datetime import datetime

from exceptions import NotFoundError


class Fildactualite:
    """Classe contenant les méthodes de service pour le fil d'actualité"""
    @log
    def __init__(self):
        self.utilisateur_dao = UtilisateurDao()
        self.abonnement_dao = AbonnementDao()
        self.activite_dao = ActiviteDao()
    
    @log
    def creer_fil_dactualite(self, id_utilisateur: int) -> list:
        """Retourne le fil d'actualité d'un utilisateur"""
        if not UtilisateurDao().verifier_id_existant(id_utilisateur):
            raise NotFoundError(f"Cet utilisateur n'existe pas")
        
        set_id_suivis = AbonnementService().lister_utilisateurs_suivis(id_utilisateur)
        ls_activites = []
        for u in set_id_suivis:
            ls_activites += self.activite_dao.lister_par_utilisateur(u)
        ls_activites = sorted(ls_activites, key=lambda a: a.date_activite, reverse=True)
        
        return ls_activites