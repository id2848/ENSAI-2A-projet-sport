from datetime import date, datetime
from typing import Optional
import re


class Utilisateur:
    """
    Classe représentant un Utilisateur

    Attributes
    ----------
    id_utilisateur : int
        identifiant unique
    pseudo : str
        pseudo de l'utilisateur
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
        nom: str,
        prenom: str,
        date_de_naissance: date,
        sexe: str,
        id_utilisateur: Optional[int] = None
    ):
        self.id_utilisateur = id_utilisateur
        self.pseudo = pseudo
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

    @staticmethod
    def valider_pseudo(pseudo: str) -> bool:
        """Valider que le pseudo est valide (entre 5 et 10 caractères)"""
        return len(pseudo) >= 5 and len(pseudo) <= 10 and pseudo.isalnum()
    
    @staticmethod
    def valider_nom_prenom(nom: str, prenom: str) -> bool:
        """Valider que le nom et prénom ne contiennent que des lettres et des espaces"""
        pattern = "^[A-Za-zÀ-ÿ ]+$"  # Autorise les lettres et les espaces
        return bool(re.match(pattern, nom)) and bool(re.match(pattern, prenom))

    @staticmethod
    def valider_date_naissance(date_de_naissance: str) -> bool:
        """Valider que la date de naissance est au format YYYY-MM-DD"""
        try:
            datetime.strptime(date_de_naissance, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def valider_sexe(sexe: str) -> bool:
        """Valider que le sexe est homme, femme ou autre autre"""
        return sexe.lower() in ['homme', 'femme', 'autre']
