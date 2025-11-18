from tabulate import tabulate

from utils.log_decorator import log
from utils.securite import hash_password

from business_object.joueur import Joueur
from business_object.abonnement import Abonnement

from dao.abonnement_dao import AbonnementDao
from dao.joueur_dao import JoueurDao


class AbonnementService:
    """Classe contenant les méthodes de service de Abonnement"""

    @log
    def creer_abonnement(self, id_utilisateur_suiveur, id_utilisateur_suivi) -> Joueur:
        """Créer un abonnement"""
        try:
            nouveau_abonnement = Abonnement(
                id_utilisateur_suiveur=id_utilisateur_suiveur,
                id_utilisateur_suivi=id_utilisateur_suivi,
            )
            return nouveau_abonnement if AbonnementDao().creer(nouveau_abonnement) else None
        except Exception as e:
            print(f"Erreur lors de la création de l'abonnement : {e}")
            return False        

    @log
    def supprimer_abonnement(self, id_utilisateur_suiveur, id_utilisateur_suivi) -> bool:
        """Supprimer un abonnement"""
        try:
            abonnement = Abonnement(id_utilisateur_suiveur, id_utilisateur_suivi)
            return AbonnementDao().supprimer(abonnement)
        except Exception as e:
            print(f"Erreur lors de la suppression de l'abonnement : {e}")
            return False

    @log
    def lister_utilisateurs_suivis(self, id_utilisateur):
        """Lister tous les utilisateurs suivis par un utilisateur donné
        """
        try:
            liste_abonnements = AbonnementDao().lister_suivis(id_utilisateur)
            utilisateurs_suivis = set()
            for j in liste_abonnements:
                utilisateurs_suivis.add(j.id_utilisateur_suivi)
            return utilisateurs_suivis
        except Exception as e:
            print(f"Erreur lors de la récupération des utilisateurs suivis : {e}")
            return None

    @log
    def lister_utilisateurs_suiveurs(self, id_utilisateur):
        """Lister tous les utilisateurs suiveurs par un utilisateur donné
        """
        try:
            liste_abonnements = AbonnementDao().lister_suiveurs(id_utilisateur)
            utilisateurs_suiveurs = set()
            for j in liste_abonnements:
                utilisateurs_suiveurs.add(j.id_utilisateur_suiveur)
            return utilisateurs_suiveurs
        except Exception as e:
            print(f"Erreur lors de la récupération des utilisateurs suiveurs : {e}")
            return None
