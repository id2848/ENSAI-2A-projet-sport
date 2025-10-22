class Abonnement : 

    """
    Classe représentant un abonnement entre deux utilisateurs.
    Un utilisateur (suiveur) s'abonne à un autre utilisateur (suivi).
    """

    def __init__(self, id_utilisateur_suiveur: int, id_utilisateur_suivi: int):
        """
        Initialise un nouvel abonnement.
        
        Arguments:
            id_utilisateur_suiveur: ID de l'utilisateur qui suit
            id_utilisateur_suivi: ID de l'utilisateur qui est suivi
        """
        self._id_utilisateur_suiveur = id_utilisateur_suiveur
        self._id_utilisateur_suivi = id_utilisateur_suivi
    
    def id_utilisateur_suiveur(self) -> int:
        """Retourne l'ID de l'utilisateur suiveur."""
        return self._id_utilisateur_suiveur

    def id_utilisateur_suivi(self) -> int:
        """Retourne l'ID de l'utilisateur suivi."""
        return self._id_utilisateur_suivi    
    
# Exemple d'utilisation
if __name__ == "__main__":
    # Création d'un abonnement : utilisateur 1 suit utilisateur 2
    abonnement = Abonnement(id_utilisateur_suiveur=1, id_utilisateur_suivi=2)
    
    print(abonnement)
    print(f"Suiveur: {abonnement.id_utilisateur_suiveur}")
    print(f"Suivi: {abonnement.id_utilisateur_suivi}")

    




