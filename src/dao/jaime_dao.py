import logging

from typing import List

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.jaime import Jaime

from exceptions import DatabaseCreationError, DatabaseDeletionError

class JaimeDao:
    """Classe contenant les méthodes pour accéder aux Jaimes de la base de données"""

    @log
    def creer(self, jaime: Jaime) -> Jaime:
        """Création d'un jaime dans la base de données

        Parameters
        ----------
        jaime : Jaime
            Le jaime à insérer

        Returns
        -------
        Jaime
            Le jaime inséré dans la base de données
        """
        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO jaime(id_activite, id_auteur) VALUES            "
                        "(%(id_activite)s, %(id_auteur)s)                            "
                        "  RETURNING id_activite, id_auteur;                         ",
                        {
                            "id_activite": jaime.id_activite,
                            "id_auteur": jaime.id_auteur
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.error(f"Erreur lors de la création d'un jaime : {e}")
            raise

        if res is None:
            msg_err = "Echec de la création du jaime : aucune ligne retournée par la base"
            logging.error(msg_err)
            raise DatabaseCreationError(msg_err)
        
        return jaime
    
    @log
    def lister_par_activite(self, id_activite: int) -> List[Jaime]:
        """Lister tous les jaimes d'une activité

        Parameters
        ----------
        id_activite : int
            L'identifiant de l'activité

        Returns
        -------
        List[Jaime]
            La liste de tous les jaimes d'une activité
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                               "
                        "  FROM jaime                           "
                        "  WHERE id_activite= %(id_activite)s;  ",
                        {"id_activite": id_activite}
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des jaimes d'une activité : {e}")
            raise

        liste_jaimes = []

        if res:
            for row in res:
                jaime = Jaime(
                    id_activite=row["id_activite"],
                    id_auteur=row["id_auteur"]
                )

                liste_jaimes.append(jaime)

        return liste_jaimes


    @log
    def supprimer(self, id_activite: int, id_auteur: int) -> bool:
        """Suppression d'un jaime dans la base de données

        Parameters
        ----------
        id_activite : int
            L'id de l'activité du jaime à supprimer
        id_auteur : int
            L'id de l'auteur du jaime à supprimer

        Returns
        -------
            True si le jaime a bien été supprimé
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM jaime                      "
                        "WHERE id_activite = %(id_activite)s    "
                        "AND id_auteur = %(id_auteur)s          ",
                        {
                            "id_activite": id_activite,
                            "id_auteur": id_auteur
                        }
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.error(f"Erreur lors de la suppression d'un jaime : {e}")
            raise

        if res < 1:
            msg_err = "Echec de la suppression du jaime : aucune ligne retournée par la base"
            logging.error(msg_err)
            raise DatabaseDeletionError(msg_err)
        
        return True
    
    @log
    def existe(self, id_activite: int, id_auteur: int) -> bool:
        """Vérifie si un jaime existe déjà dans la base de données

        Parameters
        ----------
        id_activite : int
            L'identifiant de l'activité
        id_auteur : int
            L'identifiant de l'auteur
        
        Returns
        -------
        bool
            True si un jaime existe, False sinon
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT 1 FROM jaime "
                        "WHERE id_activite = %(id_activite)s "
                        "AND id_auteur = %(id_auteur)s LIMIT 1;",
                        {
                            "id_activite": id_activite,
                            "id_auteur": id_auteur
                        }
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.error(f"Erreur lors de la vérification d'un jaime : {e}")
            raise
        
        return res is not None

    @log
    def compter_par_activite(self, id_activite: int) -> int:
        """Compte le nombre de jaimes pour une activité donnée.

        Parameters
        ----------
        id_activite : int
            L'identifiant de l'activité

        Returns
        -------
        int
            Nombre de jaimes pour l'activité
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT COUNT(*) FROM jaime WHERE id_activite = %(id_activite)s;",
                        {"id_activite": id_activite}
                    )
                    res = cursor.fetchone()
                    return res['count']
        except Exception as e:
            logging.error(f"Erreur lors du comptage des jaimes : {e}")
            raise
