import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.commentaire import Commentaire
from business_object.utilisateur import Utilisateur



class CommentaireDao:
    """Classe contenant les méthodes pour accéder aux Commentaires de la base de données"""
    def creer(self, utilisateur: Utilisateur) -> bool:
        """Creation d'un commentaire dans la base de données

        Parameters
        ----------
        commentaire : Commentaire

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
                        "INSERT INTO commentaire(id_activite, id_auteur, commentaire, date_commentaire) VALUES        "
                        "(%(id_activite)s, %(id_auteur)s, %(commentaire)s, %(date_commentaire)s)             "
                        "  RETURNING id_commentaire;                                                ",
                        {
                            "id_activite": commentaire.id_activite,
                            "id_auteur": commentaire.id_auteur,
                            "commentaire": commentaire.commentaire,
                            "date_commentaire": commentaire.date_commentaire,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        created = False
        if res:
            commentaire.id_commentaire = res["id_commentaire"]
            created = True

        return created
    
    @log
    def lister_par_activite(self, id_activite) -> list[Commentaire]:
        """lister tous les commentaires

        Parameters
        ----------
        None

        Returns
        -------
        liste_commentaires : list[Commentaire]
            renvoie la liste de tous les commentaires dans la base de données
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                              "
                        "  FROM commentaire                        "
                        "  WHERE id_activite= %(id_activite)s;  ",
                        {"id_activite": id_activite},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)
            raise

        liste_commentaires = []

        if res:
            for row in res:
                commentaire = Commentaire(
                    id_activite=row["id_activite"],
                    id_auteur=row["id_auteur"],
                    commentaire=row["commentaire"],
                    date_commentaire=row["date_commentaire"],
                )

                liste_commentaires.append(commentaire)

        return liste_commentaires


    @log
    def supprimer(self, commentaire) -> bool:
        """Suppression d'un commentaire dans la base de données

        Parameters
        ----------
        commentaire : Commentaire
            commentaire à supprimer de la base de données

        Returns
        -------
            True si le commentaire a bien été supprimé
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Supprimer le commentaire
                    cursor.execute(
                        "DELETE FROM commentaire                  "
                        " WHERE id_commentaire=%(id_commentaire)s      ",
                        {"id_commentaire": commentaire.id_commentaire},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)
            raise

        return res > 0