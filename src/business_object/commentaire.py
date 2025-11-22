from datetime import date
from typing import Optional


class Commentaire:
    """Classe représentant un Commentaire

    Attributes
    ----------
    id_commentaire : int
        identifiant unique
    id_activite : int
        identifiant unique
    id_auteur : int
        identifiant unique
    contenu : str
        contenu (texte) du commentaire
    date_commentaire : date
        date et heure du commentaire
    """

    def __init__(
        self,
        id_activite : int,
        id_auteur : int,
        contenu : str,
        date_commentaire : date,
        id_commentaire: Optional[int] = None
    ):
        self.id_commentaire = id_commentaire
        self.id_activite = id_activite
        self.id_auteur = id_auteur
        self.contenu = contenu
        self.date_commentaire = date_commentaire
        
    def __repr__(self) -> str:
        return (
            f"Commentaire(id_commentaire={self.id_commentaire!r}, "
            f"id_activite={self.id_activite!r}, "
            f"id_auteur={self.id_auteur!r}, "
            f"contenu={self.contenu!r}, "
            f"date_commentaire={self.date_commentaire!r} "
        )