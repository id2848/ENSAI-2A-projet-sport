from tabulate import tabulate
from utils.log_decorator import log

from dao.activite_dao import ActiviteDao
from business_object.activite import Activite


class ServiceStatistiques:
    """Classe contenant les méthodes de service pour les statistiques des activités"""

    def __init__(self):
        self.activite_dao = ActiviteDao()

    @log
    def calculer_nombre_activites(self, id_utilisateur: int) -> int:
        """Retourne le nombre d'activités d'un utilisateur"""
        liste_activites = self.activite_dao.lister_par_utilisateur(id_utilisateur)
        return len(liste_activites)

    @log
    def calculer_distance_totale(self, id_utilisateur: int) -> float:
        """Retourne la distance totale parcourue par l'utilisateur"""
        liste_activites = self.activite_dao.lister_par_utilisateur(id_utilisateur)
        return sum(a.distance for a in liste_activites)

    @log
    def calculer_duree_totale(self, id_utilisateur: int) -> int:
        """Retourne la durée totale (en secondes) des activités de l'utilisateur"""
        liste_activites = self.activite_dao.lister_par_utilisateur(id_utilisateur)
        return int(sum(a.duree.total_seconds() for a in liste_activites))
