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
            id_utilisateur_suiveur=id_joueur,
            id_utilisateur_suivi=id_joueur,
        )
        return nouveau_abonnement if AbonnementDao().creer(nouveau_abonnement) else None

    @log
    def supprimer_abonnement(self, abonnement) -> bool:
        """Supprimer un abonnement"""
        return AbonnementDao().supprimer(abonnement)

    @log
    def lister_utilisateurs_suivis(self) -> list[Joueur]:
        """Lister tous les joueurs qui sont suivis par abonnement
        """
        joueurs = JoueurDao().lister_tous()
        abonnements = AbonnementDao().lister_suivis
        utilisateurs_suivis <- set()
        for j in joueurs:
                id1 = j.id_joueur
                for k in abonnements:
                    id2 = k.id_joueur
                    if id1 == id2:
                        utilisateurs_suivis.add(j)
        return utilisateurs_suivis

    @log
    def lister_utilisateurs_suiveurs(self) -> list[Joueur]:
        """Lister tous les joueurs suiveurs par abonnement
        """
        joueurs = JoueurDao().lister_tous()
        abonnements = AbonnementDao().lister_suiveurs
        utilisateurs_suiveurs <- set()
        for j in joueurs:
                id1 = j.id_joueur
                for k in abonnements:
                    id2 = k.id_joueur
                    if id1 == id2:
                        utilisateurs_suiveurs.add(j)
        return utilisateurs_suiveurs