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

""" A POURSUIVRE

    @log
    def lister_utilisateurs_suivis(self) -> list[Joueur]:
        """Lister tous les joueurs qui sont suivis par abonnement
        """
        joueurs = JoueurDao().lister_tous()
        if not inclure_mdp:
            for j in joueurs:
                j.mdp = None
        return joueurs

lister_tous(self) -> list[Joueur]:
lister_suivis(self, id_utilisateur: int) -> list[Abonnement]:
"""
