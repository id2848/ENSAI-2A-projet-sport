from typing import List

from utils.log_decorator import log

from business_object.abonnement import Abonnement

from dao.abonnement_dao import AbonnementDao
from dao.utilisateur_dao import UtilisateurDao

from exceptions import NotFoundError, AlreadyExistsError


class AbonnementService:
    """Classe contenant les méthodes de service de Abonnement"""

    @log
    def creer_abonnement(
        self, id_utilisateur_suiveur: int, id_utilisateur_suivi: int
    ) -> Abonnement:
        """Créer un abonnement"""
        if not UtilisateurDao().verifier_id_existant(id_utilisateur_suiveur):
            raise NotFoundError(
                f"L'utilisateur avec l'id {id_utilisateur_suiveur} n'existe pas"
            )
        if not UtilisateurDao().verifier_id_existant(id_utilisateur_suivi):
            raise NotFoundError(
                f"L'utilisateur avec l'id {id_utilisateur_suivi} n'existe pas"
            )
        if self.abonnement_existe(id_utilisateur_suiveur, id_utilisateur_suivi):
            raise AlreadyExistsError("L'abonnement existe déjà")

        abonnement = Abonnement(
            id_utilisateur_suiveur=id_utilisateur_suiveur,
            id_utilisateur_suivi=id_utilisateur_suivi,
        )
        return AbonnementDao().creer(abonnement)

    @log
    def supprimer_abonnement(
        self, id_utilisateur_suiveur: int, id_utilisateur_suivi: int
    ) -> bool:
        """Supprimer un abonnement"""
        if not UtilisateurDao().verifier_id_existant(id_utilisateur_suiveur):
            raise NotFoundError(
                f"L'utilisateur avec l'id {id_utilisateur_suiveur} n'existe pas"
            )
        if not UtilisateurDao().verifier_id_existant(id_utilisateur_suivi):
            raise NotFoundError(
                f"L'utilisateur avec l'id {id_utilisateur_suivi} n'existe pas"
            )

        if not self.abonnement_existe(id_utilisateur_suiveur, id_utilisateur_suivi):
            raise NotFoundError("L'abonnement n'existe pas")

        return AbonnementDao().supprimer(id_utilisateur_suiveur, id_utilisateur_suivi)

    @log
    def lister_utilisateurs_suivis(self, id_utilisateur: int) -> List[int]:
        """Lister tous les ids des utilisateurs suivis par un utilisateur donné"""
        if not UtilisateurDao().verifier_id_existant(id_utilisateur):
            raise NotFoundError(
                f"L'utilisateur avec l'id {id_utilisateur} n'existe pas"
            )

        liste_abonnements = AbonnementDao().lister_suivis(id_utilisateur)
        utilisateurs_suivis = set()
        for j in liste_abonnements:
            utilisateurs_suivis.add(j.id_utilisateur_suivi)
        return utilisateurs_suivis

    @log
    def lister_utilisateurs_suiveurs(self, id_utilisateur: int) -> List[int]:
        """Lister tous les ids des utilisateurs suiveurs par un utilisateur donné"""
        if not UtilisateurDao().verifier_id_existant(id_utilisateur):
            raise NotFoundError(
                f"L'utilisateur avec l'id {id_utilisateur} n'existe pas"
            )

        liste_abonnements = AbonnementDao().lister_suiveurs(id_utilisateur)
        utilisateurs_suiveurs = set()
        for j in liste_abonnements:
            utilisateurs_suiveurs.add(j.id_utilisateur_suiveur)
        return utilisateurs_suiveurs

    @log
    def abonnement_existe(
        self, id_utilisateur_suiveur: int, id_utilisateur_suivi: int
    ) -> bool:
        """Vérifie si un abonnement existe dans la base de données"""
        if not UtilisateurDao().verifier_id_existant(id_utilisateur_suiveur):
            raise NotFoundError(
                f"L'utilisateur avec l'id {id_utilisateur_suiveur} n'existe pas"
            )
        if not UtilisateurDao().verifier_id_existant(id_utilisateur_suivi):
            raise NotFoundError(
                f"L'utilisateur avec l'id {id_utilisateur_suivi} n'existe pas"
            )

        abonnement = AbonnementDao().trouver_par_ids(
            id_utilisateur_suiveur, id_utilisateur_suivi
        )
        return abonnement is not None
