class Jaime:
    """Classe représentant un Jaime

    Attributes
    ----------
    id_activite : int
        identifiant de l'activité aimée
    id_auteur : int
        identifiant de l'utilisateur qui aime
    """

    def __init__(self, id_activite: int, id_auteur: int):
        self.id_activite = id_activite
        self.id_auteur = id_auteur

    def __repr__(self) -> str:
        return f"id_activite={self.id_activite!r}, " f"id_auteur={self.id_auteur!r}, "
