import logging

from utils.log_decorator import log

from dao.activite_dao import ActiviteDao
from business_object.activite import Activite

from dao.utilisateur_dao import UtilisateurDao

from datetime import datetime
from utils.verifier_date import verifier_date


class StatistiquesService:
    """Classe contenant les méthodes de service pour les statistiques des activités"""

    def __init__(self):
        self.activite_dao = ActiviteDao()
        self.utilisateur_dao = UtilisateurDao()

    def verifier_utilisateur_existant(self, id_utilisateur: int) -> bool:
        """Vérifie si l'utilisateur existe dans la base de données"""
        # Logique pour vérifier si l'utilisateur existe. Exemple :
        utilisateur = self.utilisateur_dao.trouver_par_id(id_utilisateur)
        return utilisateur is not None

    @log
    def calculer_nombre_activites_total(self, id_utilisateur: int) -> dict:
        """Retourne le nombre total d'activités par sport pour un utilisateur."""
        # Validation de l'existence de l'utilisateur
        if not self.verifier_utilisateur_existant(id_utilisateur):
            logging.error(f"Utilisateur avec ID {id_utilisateur} n'existe pas.")
            return None

        liste_activites = self.activite_dao.lister_par_utilisateur(id_utilisateur)
        stats = {}
        for a in liste_activites:
            stats[a.sport] = stats.get(a.sport, 0) + 1
        return stats

    @log
    def calculer_distance_totale(self, id_utilisateur: int) -> float:
        """Retourne la distance totale parcourue par l'utilisateur."""
        # Validation de l'existence de l'utilisateur
        if not self.verifier_utilisateur_existant(id_utilisateur):
            logging.error(f"Utilisateur avec ID {id_utilisateur} n'existe pas.")
            return None

        liste_activites = self.activite_dao.lister_par_utilisateur(id_utilisateur)
        return sum(a.distance for a in liste_activites)

    @log
    def calculer_duree_totale(self, id_utilisateur: int) -> int:
        """Retourne la durée totale (en secondes) des activités de l'utilisateur."""
        # Validation de l'existence de l'utilisateur
        if not self.verifier_utilisateur_existant(id_utilisateur):
            logging.error(f"Utilisateur avec ID {id_utilisateur} n'existe pas.")
            return None

        liste_activites = self.activite_dao.lister_par_utilisateur(id_utilisateur)
        duree_totale = 0
        for a in liste_activites:
            if isinstance(a.duree, (int, float)):
                duree_totale += int(a.duree * 60)  # Conversion minutes → secondes
            else:
                duree_totale += int(a.duree.total_seconds())
        return duree_totale

    @log
    def calculer_nombre_activites_semaine(self, id_utilisateur: int, date_reference: str) -> dict:
        """Retourne le nombre d'activités par sport pour la semaine correspondant à la date donnée."""
        # Validation de l'existence de l'utilisateur
        if not self.verifier_utilisateur_existant(id_utilisateur):
            logging.error(f"Utilisateur avec ID {id_utilisateur} n'existe pas.")
            return None
        
        # Validation du format de la date
        if not verifier_date(date_reference):
            logging.error(f"Le format de la date {date_reference} est incorrect. Utilisez le format YYYY-MM-DD.")
            return None
        
        date_reference_obj = datetime.strptime(date_reference, "%Y-%m-%d").date()
        liste_activites = self.activite_dao.lister_par_utilisateur(id_utilisateur)
        semaine_ref = date_reference_obj.isocalendar().week
        annee_ref = date_reference_obj.isocalendar().year

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
    def calculer_distance_semaine(self, id_utilisateur: int, date_reference: str) -> float:
        """Retourne la distance totale parcourue par semaine (tous sports confondus)."""
        # Validation de l'existence de l'utilisateur
        if not self.verifier_utilisateur_existant(id_utilisateur):
            logging.error(f"Utilisateur avec ID {id_utilisateur} n'existe pas.")
            return None
        
        # Validation du format de la date
        if not verifier_date(date_reference):
            logging.error(f"Le format de la date {date_reference} est incorrect. Utilisez le format YYYY-MM-DD.")
            return None
        
        date_reference_obj = datetime.strptime(date_reference, "%Y-%m-%d").date()
        liste_activites = self.activite_dao.lister_par_utilisateur(id_utilisateur)
        semaine_ref = date_reference_obj.isocalendar().week
        annee_ref = date_reference_obj.isocalendar().year

        activites_semaine = [
            a for a in liste_activites
            if a.date_activite.isocalendar().week == semaine_ref
            and a.date_activite.isocalendar().year == annee_ref
        ]

        return sum(a.distance for a in activites_semaine)

    @log
    def calculer_duree_semaine(self, id_utilisateur: int, date_reference: str) -> int:
        """Retourne la durée totale (en secondes) des activités de la semaine."""
        # Validation de l'existence de l'utilisateur
        if not self.verifier_utilisateur_existant(id_utilisateur):
            logging.error(f"Utilisateur avec ID {id_utilisateur} n'existe pas.")
            return None
        
        # Validation du format de la date
        if not verifier_date(date_reference):
            logging.error(f"Le format de la date {date_reference} est incorrect. Utilisez le format YYYY-MM-DD.")
            return None
        
        date_reference_obj = datetime.strptime(date_reference, "%Y-%m-%d").date()
        liste_activites = self.activite_dao.lister_par_utilisateur(id_utilisateur)
        semaine_ref = date_reference_obj.isocalendar().week
        annee_ref = date_reference_obj.isocalendar().year

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
        