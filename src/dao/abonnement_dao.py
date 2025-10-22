import logging
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.abonnement import Abonnement
class AbonnementDao:
    """Classe contenant les méthodes pour accéder aux abonnements de la base de données"""

    @log
    def creer(self, abonnement: Abonnement) -> bool:
        """Création d'un abonnement dans la base de données

        Parameters
        ----------
        abonnement : Abonnement

        Returns
        -------
        created : bool
            True si la création est un succès
            False sinon
        """
        res = None

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
            logging.info(e)

        created = False
        if res:
            created = True

        return created
    @log
    def trouver_par_ids(self, id_utilisateur_suiveur: int, id_utilisateur_suivi: int) -> Abonnement:
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
            renvoie l'abonnement que l'on cherche
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
            logging.info(e)
            raise

        abonnement = None
        if res:
            abonnement = Abonnement(
                id_utilisateur_suiveur=res["id_utilisateur_suiveur"],
                id_utilisateur_suivi=res["id_utilisateur_suivi"],
            )

        return abonnement
    @log
    def lister_suivis(self, id_utilisateur: int) -> list[Abonnement]:
        """Lister tous les abonnements d'un utilisateur (personnes qu'il suit)

        Parameters
        ----------
        id_utilisateur : int
            ID de l'utilisateur dont on veut la liste des suivis

        Returns
        -------
        liste_abonnements : list[Abonnement]
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
            logging.info(e)
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
    def lister_suiveurs(self, id_utilisateur: int) -> list[Abonnement]:
        """Lister tous les abonnements d'un utilisateur (personnes qui le suivent)

        Parameters
        ----------
        id_utilisateur : int
            ID de l'utilisateur dont on veut la liste des suiveurs

        Returns
        -------
        liste_abonnements : list[Abonnement]
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
            logging.info(e)
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
    def lister_tous(self) -> list[Abonnement]:
        """Lister tous les abonnements

        Returns
        -------
        liste_abonnements : list[Abonnement]
            renvoie la liste de tous les abonnements dans la base de données
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *              "
                        "  FROM abonnement;    "
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)
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
    def supprimer(self, abonnement: Abonnement) -> bool:
        """Suppression d'un abonnement dans la base de données

        Parameters
        ----------
        abonnement : Abonnement
            abonnement à supprimer de la base de données

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
                            "id_utilisateur_suiveur": abonnement.id_utilisateur_suiveur,
                            "id_utilisateur_suivi": abonnement.id_utilisateur_suivi,
                        },
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)
            raise

        return res > 0