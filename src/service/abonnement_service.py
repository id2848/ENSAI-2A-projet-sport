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
        """Création d'un joueur à partir de ses attributs"""

        nouveau_abonnement = Abonnement(
            id_utilisateur_suiveur=id_utilisateur_suiveur,
            id_utilisateur_suivi=id_utilisateur_suivi,
        )
        
        return nouveau_abonnement if AbonnementDao().creer(nouveau_abonnement) else None

    @log
    def supprimer_abonnement(self, abonnement) -> bool:
        """Supprimer un abonnement"""
        return AbonnementDao().supprimer(abonnement)

    @log
    def lister_utilisateurs_suivis(self, id_utilisateur):
        """Lister tous les joueurs suivis par un joueur
        """
        liste_abonnements = AbonnementDao().lister_suivis(id_utilisateur)
        utilisateurs_suivis = set()
        for j in liste_abonnements:
            utilisateurs_suivis.add(j.id_utilisateur_suivi)
        return utilisateurs_suivis

    @log
    def lister_utilisateurs_suiveurs(self, id_utilisateur):
        """Lister tous les joueurs suiveurs par un joueur
        """
        liste_abonnements = AbonnementDao().lister_suiveurs(id_utilisateur)
        utilisateurs_suiveurs = set()
        for j in liste_abonnements:
            utilisateurs_suiveurs.add(j.id_utilisateur_suiveur)
        return utilisateurs_suiveurs