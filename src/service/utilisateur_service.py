from typing import List
from datetime import date, datetime, timedelta

from utils.log_decorator import log
from utils.securite import hash_password

from business_object.utilisateur import Utilisateur
from business_object.abonnement import Abonnement
from business_object.activite import Activite
from business_object.commentaire import Commentaire
from business_object.jaime import Jaime


from dao.abonnement_dao import AbonnementDao
from dao.utilisateur_dao import UtilisateurDao
from dao.activite_dao import ActiviteDao
from dao.commentaire_dao import CommentaireDao
from dao.jaime_dao import JaimeDao

class UtilisateurService:
    """Classe contenant les méthodes de service d'Utilisateurs"""

    def lister_utilisateurs(self) -> List[Utilisateur]:
        """ Liste toutes les utilisateurs  """
        try:
            # Recherche des utilisateurs
            liste = UtilisateurDao().lister_tous()

            # Vérification si aucun utilisateur n'est trouvé
            if not liste:
                print(f"Aucun utilisateur trouvé")

            return liste  # Retourne la liste des utilisateurs (peut être vide)
    
        except Exception as e:
            # Gestion des exceptions : affichage du message d'erreur
            print(f"Erreur lors de la récupération des utilisateurs: {e}")
            return []  # Retourne une liste vide en cas d'erreur


    def trouver_par_id(self, id_utilisateur) -> Utilisateur:
        """Trouver un Utilisateur à partir de son id"""
        return UtilisateurDao().trouver_par_id(id_utilisateur)


    def trouver_par_pseudo(self, pseudo) -> Utilisateur:
        """Trouver un Utilisateur à partir de son pseudo"""
        return UtilisateurDao().trouver_par_pseudo(pseudo)