from typing import List

import logging
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.abonnement import Abonnement

from exceptions import DatabaseCreationError, DatabaseDeletionError


class AbonnementDao:
    """Classe contenant les méthodes pour accéder aux abonnements de la base de données"""

    @log
    def creer(self, abonnement: Abonnement) -> Abonnement:
        """Création d'un abonnement dans la base de données

        Parameters
        ----------
        abonnement : Abonnement
            L'abonnement à insérer

        Returns
        -------
        Abonnement
            L'abonnement inséré dans la base de données
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO abonnement(id_utilisateur_suiveur, id_utilisateur_suivi) VALUES "
                        "(%(id_utilisateur_suiveur)s, %(id_utilisateur_suivi)s)                      "
                        "  RETURNING id_utilisateur_suiveur, id_utilisateur_suivi;                   ",
                        {
                            "id_utilisateur_suiveur": abonnement.id_utilisateur_suiveur,
                            "id_utilisateur_suivi": abonnement.id_utilisateur_suivi,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.error(e)
            raise

        if res is None:
            msg_err = "Echec de la création de l'abonnement : aucune ligne retournée par la base"
            logging.error(msg_err)
            raise DatabaseCreationError(msg_err)

        return abonnement

    @log
    def trouver_par_ids(
        self, id_utilisateur_suiveur: int, id_utilisateur_suivi: int
    ) -> Abonnement | None:
        """Trouver un abonnement grâce aux ids du suiveur et du suivi

        Parameters
        ----------
        id_utilisateur_suiveur : int
            numéro id de l'utilisateur suiveur
        id_utilisateur_suivi : int
            numéro id de l'utilisateur suivi

        Returns
        -------
        abonnement : Abonnement
            Renvoie l'abonnement que l'on cherche
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                                                    "
                        "  FROM abonnement                                           "
                        " WHERE id_utilisateur_suiveur = %(id_utilisateur_suiveur)s "
                        "   AND id_utilisateur_suivi = %(id_utilisateur_suivi)s;    ",
                        {
                            "id_utilisateur_suiveur": id_utilisateur_suiveur,
                            "id_utilisateur_suivi": id_utilisateur_suivi,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.error(e)
            raise

        abonnement = None
        if res:
            abonnement = Abonnement(
                id_utilisateur_suiveur=res["id_utilisateur_suiveur"],
                id_utilisateur_suivi=res["id_utilisateur_suivi"],
            )

        return abonnement

    @log
    def lister_suivis(self, id_utilisateur: int) -> List[Abonnement]:
        """Lister tous les abonnements d'un utilisateur (personnes qu'il suit)

        Parameters
        ----------
        id_utilisateur : int
            ID de l'utilisateur dont on veut la liste des suivis

        Returns
        -------
        liste_abonnements : List[Abonnement]
            liste des abonnements où l'utilisateur est suiveur
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                                                    "
                        "  FROM abonnement                                           "
                        " WHERE id_utilisateur_suiveur = %(id_utilisateur)s;         ",
                        {"id_utilisateur": id_utilisateur},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.error(e)
            raise

        liste_abonnements = []

        if res:
            for row in res:
                abonnement = Abonnement(
                    id_utilisateur_suiveur=row["id_utilisateur_suiveur"],
                    id_utilisateur_suivi=row["id_utilisateur_suivi"],
                )
                liste_abonnements.append(abonnement)

        return liste_abonnements

    @log
    def lister_suiveurs(self, id_utilisateur: int) -> List[Abonnement]:
        """Lister tous les abonnements d'un utilisateur (personnes qui le suivent)

        Parameters
        ----------
        id_utilisateur : int
            ID de l'utilisateur dont on veut la liste des suiveurs

        Returns
        -------
        liste_abonnements : List[Abonnement]
            liste des abonnements où l'utilisateur est suivi
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                                                "
                        "  FROM abonnement                                       "
                        " WHERE id_utilisateur_suivi = %(id_utilisateur)s;       ",
                        {"id_utilisateur": id_utilisateur},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.error(e)
            raise

        liste_abonnements = []

        if res:
            for row in res:
                abonnement = Abonnement(
                    id_utilisateur_suiveur=row["id_utilisateur_suiveur"],
                    id_utilisateur_suivi=row["id_utilisateur_suivi"],
                )
                liste_abonnements.append(abonnement)

        return liste_abonnements

    @log
    def lister_tous(self) -> List[Abonnement]:
        """Lister tous les abonnements

        Returns
        -------
        liste_abonnements : List[Abonnement]
            Renvoie la liste de tous les abonnements dans la base de données
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT *              " "  FROM abonnement;    ")
                    res = cursor.fetchall()
        except Exception as e:
            logging.error(e)
            raise

        liste_abonnements = []

        if res:
            for row in res:
                abonnement = Abonnement(
                    id_utilisateur_suiveur=row["id_utilisateur_suiveur"],
                    id_utilisateur_suivi=row["id_utilisateur_suivi"],
                )
                liste_abonnements.append(abonnement)

        return liste_abonnements

    @log
    def supprimer(self, id_utilisateur_suiveur: int, id_utilisateur_suivi: int) -> bool:
        """Suppression d'un abonnement dans la base de données

        Parameters
        ----------
        id_utilisateur_suiveur: int
            l'id de l'utilisateur suiveur de l'abonnement à supprimer
        id_utilisateur_suivi: int
            l'id de l'utilisateur suivi de l'abonnement à supprimer

        Returns
        -------
        bool
            True si l'abonnement a bien été supprimé
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM abonnement                                      "
                        " WHERE id_utilisateur_suiveur = %(id_utilisateur_suiveur)s "
                        "   AND id_utilisateur_suivi = %(id_utilisateur_suivi)s;    ",
                        {
                            "id_utilisateur_suiveur": id_utilisateur_suiveur,
                            "id_utilisateur_suivi": id_utilisateur_suivi,
                        },
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.error(e)
            raise

        if not res:
            msg_err = "Echec de la suppression de l'abonnement : aucune ligne retournée par la base"
            logging.error(msg_err)
            raise DatabaseDeletionError(msg_err)

        return True
