from tabulate import tabulate
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


class Fildactualite:
    """Classe contenant les méthodes de service pour le fil d'actualité"""

    def __init__(self):
        self.utilisateur_dao = UtilisateurDao()
        self.abonnement_dao = AbonnementDao()
        self.activite_dao = ActiviteDao()
    @log
    def creer_fil_dactualite(self, id_utilisateur: int) -> list:
        """Retourne le fil d'actualité d'un utilisateur"""

        liste_id_suivis = AbonnementService().lister_utilisateurs_suivis(id_utilisateur) 
                
        for j in liste_id_suivis:
            ls_activites = self.activite_dao.lister_par_utilisateur(j)
        ls_activites = sorted(ls_activites, key=lambda a: a.date_activite)
        print(ls_activites)
        return ls_activites