from tabulate import tabulate
from utils.log_decorator import log

from dao.activite_dao import ActiviteDao
from business_object.activite import Activite


class ServiceStatistiques:
    """Classe contenant les méthodes de service pour les statistiques des activités"""

    def __init__(self):
        self.activite_dao = ActiviteDao()

    @log
    def calculer_nombre_activites_totale(self, id_utilisateur: int) -> dict:
        """Retourne le nombre total d'activités par sport pour un utilisateur."""
        
        liste_activites = self.activite_dao.lister_par_utilisateur(id_utilisateur)
        stats = {}
        for a in liste_activites:
            stats[a.sport] = stats.get(a.sport, 0) + 1
        return stats

    @log
    def calculer_distance_totale(self, id_utilisateur: int) -> float:
        """Retourne la distance totale parcourue par l'utilisateur."""

        liste_activites = self.activite_dao.lister_par_utilisateur(id_utilisateur)
        return sum(a.distance for a in liste_activites)

    @log
    def calculer_duree_totale(self, id_utilisateur: int) -> int:
        """Retourne la durée totale (en secondes) des activités de l'utilisateur."""

        liste_activites = self.activite_dao.lister_par_utilisateur(id_utilisateur)
        duree_totale = 0
        for a in liste_activites:
            if isinstance(a.duree, (int, float)):
                duree_totale += int(a.duree * 60)  # float minutes → secondes
            else:
                duree_totale += int(a.duree.total_seconds())
        return duree_totale

    @log
    def calculer_nombre_activites_semaine(self, id_utilisateur: int, date_reference) -> dict:
        """Retourne le nombre d'activités par sport pour la semaine correspondant à la date donnée."""

        liste_activites = self.activite_dao.lister_par_utilisateur(id_utilisateur)
        semaine_ref = date_reference.isocalendar().week
        annee_ref = date_reference.isocalendar().year

        activites_semaine = [
            a for a in liste_activites
            if a.date_activite.isocalendar().week == semaine_ref
            and a.date_activite.isocalendar().year == annee_ref
        ]

        stats = {}
        for a in activites_semaine:
            stats[a.sport] = stats.get(a.sport, 0) + 1
        return stats

    @log
    def calculer_distance_semaine(self, id_utilisateur: int, date_reference) -> float:
        """Retourne la distance totale parcourue par semaine (tous sports confondus)."""

        liste_activites = self.activite_dao.lister_par_utilisateur(id_utilisateur)
        semaine_ref = date_reference.isocalendar().week
        annee_ref = date_reference.isocalendar().year

        activites_semaine = [
            a for a in liste_activites
            if a.date_activite.isocalendar().week == semaine_ref
            and a.date_activite.isocalendar().year == annee_ref
        ]

        return sum(a.distance for a in activites_semaine)

    @log
    def calculer_duree_semaine(self, id_utilisateur: int, date_reference) -> int:
        """Retourne la durée totale (en secondes) des activités de la semaine."""

        liste_activites = self.activite_dao.lister_par_utilisateur(id_utilisateur)
        semaine_ref = date_reference.isocalendar().week
        annee_ref = date_reference.isocalendar().year

        activites_semaine = [
            a for a in liste_activites
            if a.date_activite.isocalendar().week == semaine_ref
            and a.date_activite.isocalendar().year == annee_ref
        ]

        duree_totale = 0
        for a in activites_semaine:
            if isinstance(a.duree, (int, float)):
                duree_totale += int(a.duree * 60)
            else:
                duree_totale += int(a.duree.total_seconds())
        return duree_totale
