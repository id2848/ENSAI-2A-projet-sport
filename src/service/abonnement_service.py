from tabulate import tabulate

from utils.log_decorator import log

from business_object.abonnement import Abonnement

from dao.abonnement_dao import AbonnementDao


class AbonnementService:
    """Classe contenant les méthodes de service de Abonnement"""

    @log
    def creer_abonnement(self, id_utilisateur_suiveur: int, id_utilisateur_suivi: int) -> Abonnement:
        """Créer un abonnement"""
        try:
            nouveau_abonnement = Abonnement(
                id_utilisateur_suiveur=id_utilisateur_suiveur,
                id_utilisateur_suivi=id_utilisateur_suivi,
            )
            return nouveau_abonnement if AbonnementDao().creer(nouveau_abonnement) else None
        except Exception as e:
            logging.error(f"Erreur lors de la création de l'abonnement : {e}")
            return False

    @log
    def supprimer_abonnement(self, id_utilisateur_suiveur: int, id_utilisateur_suivi: int) -> bool:
        """Supprimer un abonnement"""
        try:
            return AbonnementDao().supprimer(id_utilisateur_suiveur, id_utilisateur_suivi)
        except Exception as e:
            logging.error(f"Erreur lors de la suppression de l'abonnement : {e}")
            return False

    @log
    def lister_utilisateurs_suivis(self, id_utilisateur: int):
        """Lister tous les utilisateurs suivis par un utilisateur donné
        """
        try:
            liste_abonnements = AbonnementDao().lister_suivis(id_utilisateur)
            utilisateurs_suivis = set()
            for j in liste_abonnements:
                utilisateurs_suivis.add(j.id_utilisateur_suivi)
            return utilisateurs_suivis
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des utilisateurs suivis : {e}")
            return None

    @log
    def lister_utilisateurs_suiveurs(self, id_utilisateur: int):
        """Lister tous les utilisateurs suiveurs par un utilisateur donné
        """
        try:
            liste_abonnements = AbonnementDao().lister_suiveurs(id_utilisateur)
            utilisateurs_suiveurs = set()
            for j in liste_abonnements:
                utilisateurs_suiveurs.add(j.id_utilisateur_suiveur)
            return utilisateurs_suiveurs
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des utilisateurs suiveurs : {e}")
            return None
