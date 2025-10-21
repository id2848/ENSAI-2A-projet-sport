from datetime import date
from typing import Optional


class Utilisateur:
    """
    Classe représentant un Utilisateur

    Attributes
    ----------
    id_utilisateur : int
        identifiant unique
    pseudo : str
        pseudo de l'utilisateur
    mot_de_passe_hash : str
        mot de passe hashé de l'utilisateur
    nom : str
        nom de famille
    prenom : str
        prénom
    date_de_naissance : date
        date de naissance de l'utilisateur
    sexe : str
        sexe de l'utilisateur (ex: 'M', 'F', 'Autre')
    """

    def __init__(
        self,
        pseudo: str,
        mot_de_passe_hash: str,
        nom: str,
        prenom: str,
        date_de_naissance: date,
        sexe: str,
        id_utilisateur: Optional[int] = None
    ):
        self.id_utilisateur = id_utilisateur
        self.pseudo = pseudo
        self.mot_de_passe_hash = mot_de_passe_hash
        self.nom = nom
        self.prenom = prenom
        self.date_de_naissance = date_de_naissance
        self.sexe = sexe

    def __repr__(self) -> str:
        return (
            f"Utilisateur(id_utilisateur={self.id_utilisateur!r}, "
            f"pseudo={self.pseudo!r}, "
            f"nom={self.nom!r}, "
            f"prenom={self.prenom!r}, "
            f"date_de_naissance={self.date_de_naissance!r}, "
            f"sexe={self.sexe!r})"
        )

    def calculer_age(self) -> int:
        """Calcule l'âge de l'utilisateur en années."""
        today = date.today()
        return today.year - self.date_de_naissance.year - (
            (today.month, today.day) < (self.date_de_naissance.month, self.date_de_naissance.day)
        )
