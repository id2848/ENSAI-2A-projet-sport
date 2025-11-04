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
from dao.activite_dao import ActiviteDAO
from dao.commentaire_dao import CommentaireDao
from dao.jaime_dao import JaimeDao

class ActiviteService:
    """Classe contenant les méthodes de service des activités Utilisateurs"""

    def creer_activite(self, id_utilisateur: int, sport: str,date_activite: date, distance: float, 
        duree: timedelta) -> bool:
        """ Crée une nouvelle activité """
        try:
            # Logique pour créer une nouvelle activité
            activite = Activite(id_utilisateur=id_utilisateur, sport=sport, date_activite=datetime.now(), distance= distance, duree= duree)
            return True
        except Exception as e:
            print(f"Erreur lors de la création de l'activité : {e}")
            return False

    def supprimer_activite(self, id_activite: int) -> bool:
        """ Supprime une activité existante """
        try:
            activite = ActiviteDAO.trouver_par_id(id_activite=id_activite)  # Récupère l'activité par son ID
        
            # Si l'activité n'existe pas
            if activite is None:
                print(f"L'activité avec ID {id_activite} n'existe pas.")
            return False
        
            ActiviteDAO.supprimer(id_activite=id_activite)  # Effectue la suppression dans la base de données
            return True
        
        except Exception as e:
            print(f"Erreur lors de la suppression de l'activité : {e}")
            return False

    def modifier_activite(self, id_activite: int, sport: str) -> bool:
        """ Modifie une activité existante """
        try:
            activite = ActiviteDAO.trouver_par_id(id_activite=id_activite)  # Récupère l'activité par son ID
            # Si l'activité n'existe pas
            if activite is None:
                print(f"L'activité avec ID {id_activite} n'existe pas.")
            return False
        
            activite.sport = sport  # Modification du sport de l'activité
            ActiviteDAO.modifier(activite)
            return True
        
        except Exception as e:
            print(f"Erreur lors de la modification de l'activité : {e}")
            return False


    def lister_activites(self, id_utilisateur: int) -> List[Activite]:
        """ Liste toutes les activités d'un utilisateur donné """
        try:
            # Recherche des activités par utilisateur
            activites = ActiviteDAO.lister_par_utilisateur(id_utilisateur=id_utilisateur)

            # Vérification si aucune activité n'est trouvée
            if not activites:
                print(f"Aucune activité trouvée pour l'utilisateur avec ID {id_utilisateur}.")

            return activites  # Retourne la liste des activités (peut être vide)
    
        except Exception as e:
            # Gestion des exceptions : affichage du message d'erreur
            print(f"Erreur lors de la récupération des activités pour l'utilisateur {id_utilisateur}: {e}")
            return []  # Retourne une liste vide en cas d'erreur


    def ajouter_jaime(self, id_activite: int, id_utilisateur: int ) -> bool:
        """ Ajoute un "j'aime" à une activité """
        try:
            activite = ActiviteDAO.trouver_par_id(id_activite=id_activite)
            utilisateur = UtilisateurDAO.trouver_par_id(id_utilisateur=id_utilisateur)
            JaimeDao.creer(activite, utilisateur)  # Ajoute l'utilisateur à la liste des "j'aime"
            return True
        except Exception as e:
            print(f"Erreur lors de l'ajout du 'j'aime' : {e}")
            return False

    def supprimer_jaime(self, id_utilisateur: int, id_activite: int) -> bool:
        """ Supprime un "j'aime" d'une activité """
        try:
            activite = ActiviteDAO.trouver_par_id(id_activite=id_activite)
            utilisateur = UtilisateurDAO.trouver_par_id(id_utilisateur=id_utilisateur)
            JaimeDao.supprimer(activite, utilisateur)  # Retire l'utilisateur de la liste des "j'aime"
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression du 'j'aime' : {e}")
            return False

    def ajouter_commentaire(self, id_utilisateur: int, id_activite: int, commentaire: str) -> bool:
        """ Ajoute un commentaire à une activité """
        try:
            activite = ActiviteDAO.trouver_par_id(id_activite=id_activite)
            utilisateur = UtilisateurDAO.trouver_par_id(id_utilisateur=id_utilisateur)
            nouveau_commentaire = Commentaire(
            activite=activite,
            utilisateur=utilisateur,
            commentaire=commentaire,
            date_commentaire=datetime.now())
            CommentaireDao.creer(nouveau_commentaire)
            return True
        except Exception as e:
            print(f"Erreur lors de l'ajout du commentaire : {e}")
            return False

    def supprimer_commentaire(self, id_commentaire: int) -> bool:
        """Supprime un commentaire d'une activité"""
        try:
            # Récupérer le commentaire par son ID
            commentaire = CommentaireDao.trouver_par_id(id_commentaire=id_commentaire)

            # Si le commentaire n'existe pas
            if commentaire is None:
                print(f"Le commentaire avec ID {id_commentaire} n'existe pas.")
                return False

            # Supprimer le commentaire de la base de données
            CommentaireDao.supprimer(commentaire)
            return True

        except Exception as e:
            print(f"Erreur lors de la suppression du commentaire : {e}")
            return False

    def lister_commentaires(self, id_activite: int) -> List[Commentaire]:
        """ Liste tous les commentaires d'une activité """
        try:
             commentaires = CommentaireDAO.lister_par_activite(id_activite=id_activite)  # Méthode dans le DAO
             return commentaires
        except Exception as e:
            print(f"Erreur lors de la récupération des commentaires : {e}")
            return []

    def placeholder(self) -> bool:
        """Méthode temporaire pour garder la pipeline verte
        A supprimer quand de vraies méthodes seront créées et testées"""

        return True
