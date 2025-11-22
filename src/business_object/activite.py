from datetime import date

from typing import Optional

from utils.utils_date import valider_date

class Activite: 
    """Classe représentant les différentes activités que l'utilisateur peut faire. 

    Attributes
    ----------
    id_activite : int 
        identifiant unique
    id_utilisateur : int 
        identifiant unique
    sport : str
        énumeration de sport
    date_activite : date
        date à laquelle a été réalisée l'activité, construit avec une date ou un str au format YYYY-MM-DD
    distance : float 
        distance parcourue en km
    duree : float 
        temps de l'activité en minutes
    """

    def __init__(
        self,
        id_utilisateur: int, 
        sport: str, 
        date_activite: date | str, 
        distance: float, 
        duree: float,
        id_activite: Optional[int] = None
    ):
        self.id_activite = id_activite
        self.id_utilisateur = id_utilisateur
        self.sport = self.valider_sport(sport)
        self.date_activite = self.valider_date_activite(date_activite)
        self.distance = distance
        self.duree = duree

    def __repr__(self):
        return (f"Activite(id_activite={self.id_activite}, "
                f"id_utilisateur={self.id_utilisateur}, "
                f"sport={self.sport}, "
                f"date_activite={self.date_activite}, "
                f"distance={self.distance} km, "
                f"duree={self.duree} minutes)")
    
    def calculer_vitesse(self) -> float:
        """Calcule la vitesse moyenne en km/h."""
        heures = self.duree / 60
        return self.distance / heures if heures > 0 else 0.0
    
    @staticmethod
    def valider_sport(sport: str) -> str:
        """Valider que le sport est 'course', 'natation', 'vélo', 'randonnée' ou 'autre'"""
        if not isinstance(sport, str):
            raise ValueError("sport doit être un str")
        sport = sport.lower()
        if not sport in ['course', 'natation', 'vélo', 'randonnée', 'autre']:
            raise ValueError("Sport invalide. Il doit être 'course', 'natation', 'vélo', 'randonnée' ou 'autre'")
        return sport

    @staticmethod
    def valider_date_activite(date_activite: date | str) -> date:
        """Valider que la date de l'activité est une date ou bien un str au format YYYY-MM-DD
        Renvoie un objet 'date'"""
        try:
            return valider_date(date_activite)
        except ValueError:
            raise ValueError("date_activite doit être un objet 'date' ou un str au format YYYY-MM-DD")
