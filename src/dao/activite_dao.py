import logging
from utils.log_decorator import log

from typing import List

from dao.db_connection import DBConnection

from business_object.activite import Activite

from exceptions import DatabaseCreationError, DatabaseDeletionError, DatabaseUpdateError


class ActiviteDao:
    """Classe contenant les méthodes pour accéder aux activités de la base de données"""

    @log
    def creer(self, activite: Activite) -> Activite:
        """Création d'une activité dans la base de données

        Parameters
        ----------
        activite : Activite
            L'activité à insérer dans la base

        Returns
        -------
        Activite
            L'activité insérée, avec son identifiant mis à jour
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO activite(
                            id_utilisateur, sport, date_activite, distance, duree
                        )
                        VALUES (
                            %(id_utilisateur)s, %(sport)s,
                            %(date_activite)s, %(distance)s, %(duree)s
                        )
                        RETURNING id_activite;
                        """,
                        {
                            "id_utilisateur": activite.id_utilisateur,
                            "sport": activite.sport,
                            "date_activite": activite.date_activite,
                            "distance": activite.distance,
                            "duree": activite.duree,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.error(f"Erreur lors de la création d'une activité : {e}")
            raise

        if res is None:
            msg_err = "Echec de la création de l'activité : aucune ligne retournée par la base"
            logging.error(msg_err)
            raise DatabaseCreationError(msg_err)

        activite.id_activite = res["id_activite"]
        return activite

    @log
    def trouver_par_id(self, id_activite: int) -> Activite | None:
        """Trouver une activité par son identifiant

        Parameters
        ----------
        id_activite : int
            L'identifiant de l'activité recherchée

        Returns
        -------
        Activite | None
            L'activité correspondante si trouvée, sinon None
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM activite WHERE id_activite = %(id_activite)s;",
                        {"id_activite": id_activite},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.error(e)
            raise

        activite = None
        if res:
            activite = Activite(
                id_activite=res["id_activite"],
                id_utilisateur=res["id_utilisateur"],
                sport=res["sport"],
                date_activite=res["date_activite"],
                distance=res["distance"],
                duree=res["duree"],
            )
        return activite

    @log
    def modifier(self, activite: Activite) -> bool:
        """Modifier une activité existante dans la base de données

        Parameters
        ----------
        activite : Activite
            L’activité contenant les nouvelles valeurs à mettre à jour

        Returns
        -------
        bool
            True si la modification a bien été effectuée
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE activite
                        SET id_utilisateur=%(id_utilisateur)s,
                            sport=%(sport)s,
                            date_activite=%(date_activite)s,
                            distance=%(distance)s,
                            duree=%(duree)s
                        WHERE id_activite=%(id_activite)s;
                        """,
                        {
                            "id_activite": activite.id_activite,
                            "id_utilisateur": activite.id_utilisateur,
                            "sport": activite.sport,
                            "date_activite": activite.date_activite,
                            "distance": activite.distance,
                            "duree": activite.duree,
                        },
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.error(e)
            raise

        if res < 1:
            msg_err = "Echec de la modification de l'activité : aucune ligne retournée par la base"
            logging.error(msg_err)
            raise DatabaseUpdateError(msg_err)

        return True

    @log
    def supprimer(self, id_activite: int) -> bool:
        """Supprimer une activité de la base de données

        Parameters
        ----------
        id_activite : int
            L'identifiant de l'activité à supprimer

        Returns
        -------
        bool
            True si la suppression a été réalisée
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM activite WHERE id_activite=%(id_activite)s;",
                        {"id_activite": id_activite},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.error(e)
            raise

        if res < 1:
            msg_err = "Echec de la suppression de l'activité : aucune ligne retournée par la base"
            logging.error(msg_err)
            raise DatabaseDeletionError(msg_err)

        return True

    @log
    def lister_par_utilisateur(self, id_utilisateur: int) -> List[Activite]:
        """Lister toutes les activités d'un utilisateur

        Parameters
        ----------
        id_utilisateur : int
            Identifiant de l'utilisateur dont on veut récupérer les activités

        Returns
        -------
        List[Activite]
            La liste des activités associées à l’utilisateur (liste vide si aucune)
        """
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM activite WHERE id_utilisateur = %(id_utilisateur)s;",
                        {"id_utilisateur": id_utilisateur},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.error(e)
            raise

        liste_activites = []
        if res:
            for row in res:
                activite = Activite(
                    id_activite=row["id_activite"],
                    id_utilisateur=row["id_utilisateur"],
                    sport=row["sport"],
                    date_activite=row["date_activite"],
                    distance=row["distance"],
                    duree=row["duree"],
                )
                liste_activites.append(activite)
        return liste_activites

    @log
    def lister_activites_filtres(
        self,
        id_utilisateur: int,
        sport: str = None,
        date_debut: str = None,
        date_fin: str = None,
    ) -> List[Activite]:
        """Lister les activités d'un utilisateur avec filtres optionnels

        Parameters
        ----------
        id_utilisateur : int
            Identifiant de l'utilisateur
        sport : str, optional
            Filtre sur le type de sport, par défaut None
        date_debut : str, optional
            Date minimale (incluse) au format YYYY-MM-DD, par défaut None
        date_fin : str, optional
            Date maximale (incluse) au format YYYY-MM-DD, par défaut None

        Returns
        -------
        List[Activite]
            La liste des activités correspondant aux filtres
        """

        query = "SELECT * FROM activite WHERE id_utilisateur = %(id_utilisateur)s"
        params = {"id_utilisateur": id_utilisateur}

        if sport:
            query += " AND sport = %(sport)s"
            params["sport"] = sport

        if date_debut:
            query += " AND date_activite >= %(date_debut)s"
            params["date_debut"] = date_debut

        if date_fin:
            query += " AND date_activite <= %(date_fin)s"
            params["date_fin"] = date_fin

        query += " ORDER BY date_activite DESC;"

        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                    res = cursor.fetchall()
        except Exception as e:
            logging.error(e)
            raise

        liste_activites = []
        if res:
            for row in res:
                activite = Activite(
                    id_activite=row["id_activite"],
                    id_utilisateur=row["id_utilisateur"],
                    sport=row["sport"],
                    date_activite=row["date_activite"],
                    distance=row["distance"],
                    duree=row["duree"],
                )
                liste_activites.append(activite)

        return liste_activites

    @log
    def verifier_id_existant(self, id_activite: int) -> bool:
        """Vérifier si une activité existe via son identifiant

        Parameters
        ----------
        id_activite : int
            Identifiant de l'activité à vérifier

        Returns
        -------
        bool
            True si une activité correspondant à l’id existe, False sinon
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT 1 FROM activite WHERE id_activite = %(id_activite)s;",
                        {"id_activite": id_activite},
                    )
                    res = cursor.fetchone()
                    return res is not None
        except Exception as e:
            logging.error(f"Erreur lors de la vérification de l'id {id_activite}: {e}")
            raise
