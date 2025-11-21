from datetime import date, timedelta

from typing import Optional

class Activite: 
    """
    Classe représentant les différentes activités que l'utilisateur peut faire. 

    Attributes
    ----------
    id_activite : int 
        identifiant unique
    id_utilisateur : int 
        identifiant unique
    sport : str
        énumeration de sport
    date_activite : date
        date à laquelle a été réalisée l'activité
    distance : float 
        distance parcourue
    duree : Duration 
        temps de l'activité 
    """

    def __init__(
        self,
        id_utilisateur: int, 
        sport: str, 
        date_activite: date, 
        distance: float, 
        duree: float,
        id_activite: Optional[int] = None
    ):
        self.id_activite = id_activite
        self.id_utilisateur = id_utilisateur
        self.sport = self.valider_sport(sport)
        self.date_activite = date_activite
        self.distance = distance
        self.duree = duree

    def __repr__(self):
        return (f"Activite(id_activite={self.id_activite}, "
                f"id_utilisateur={self.id_utilisateur}, "
                f"sport={self.sport}, "
                f"date_activite={self.date_activite}, "
                f"distance={self.distance} km, "
                f"duree={self.duree})")
    
    def calculer_vitesse(self) -> float:
        """Calcule la vitesse moyenne en km/h."""
        heures = self.duree.total_seconds() / 3600
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
