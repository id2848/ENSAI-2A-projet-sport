class Credentials:
    """Classe représentant les infos d'authentification d'un utilisateur
    (Non utilisée en pratique, seulement indiquée à titre de référence)

    Attributes
    ----------
    id_utilisateur : int
        identifiant de l'utilisateur
    mot_de_passe_hash : str
        mot de passe hashé de l'utilisateur
    sel : str
        sel de l'utilisateur
    """
    def __init__(
        self,
        id_utilisateur: int,
        mot_de_passe_hash: str,
        sel: str
    ):
        self.id_utilisateur = id_utilisateur
        self.mot_de_passe_hash = mot_de_passe_hash
        self.sel = sel
