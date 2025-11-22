class Abonnement:
    """Classe représentant un abonnement entre deux utilisateurs.
    Un utilisateur (suiveur) s'abonne à un autre utilisateur (suivi).

    Attributes
    ----------
    id_utilisateur_suiveur : int
        Identifiant de l'utilisateur qui suit.
    id_utilisateur_suivi : int
        Identifiant de l'utilisateur qui est suivi.
    """

    def __init__(self, id_utilisateur_suiveur: int, id_utilisateur_suivi: int):
        self.id_utilisateur_suiveur = id_utilisateur_suiveur
        self.id_utilisateur_suivi = id_utilisateur_suivi

    def __repr__(self):
        return (
            f"Abonnement(id_utilisateur_suiveur={self.id_utilisateur_suiveur!r}, "
            f"id_utilisateur_suivi={self.id_utilisateur_suivi!r})"
        )

    def __str__(self):
        return f"Abonnement: Utilisateur {self.id_utilisateur_suiveur} suit l'utilisateur {self.id_utilisateur_suivi}"


# Exemple d'utilisation
if __name__ == "__main__":
    # Création d'un abonnement : utilisateur 1 suit utilisateur 2
    abonnement = Abonnement(id_utilisateur_suiveur=1, id_utilisateur_suivi=2)

    # Création d'un abonnement : utilisateur 1 suit utilisateur 2
    abonnement = Abonnement(id_utilisateur_suiveur=1, id_utilisateur_suivi=2)

    print(abonnement)
    print(f"Suiveur: {abonnement.id_utilisateur_suiveur}")
    print(f"Suivi: {abonnement.id_utilisateur_suivi}")
