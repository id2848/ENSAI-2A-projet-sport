import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.commentaire import Commentaire
from business_object.utilisateur import Utilisateur



class CommentaireDao:
    """Classe contenant les méthodes pour accéder aux Commentaires de la base de données"""
    def creer(self, commentaire: Commentaire) -> bool:
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
                        "INSERT INTO commentaire(id_activite, id_auteur, contenu, date_commentaire) VALUES        "
                        "(%(id_activite)s, %(id_auteur)s, %(contenu)s, %(date_commentaire)s)             "
                        "  RETURNING id_commentaire;                                                ",
                        {
                            "id_activite": commentaire.id_activite,
                            "id_auteur": commentaire.id_auteur,
                            "contenu": commentaire.contenu,
                            "date_commentaire": commentaire.date_commentaire,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.error(e)

        created = False
        if res:
            commentaire.id_commentaire = res["id_commentaire"]
            created = True

        return created
    
    @log
    def lister_par_activite(self, id_activite: int) -> list[Commentaire]:
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
            logging.error(e)
            raise

        liste_commentaires = []

        if res:
            for row in res:
                commentaire = Commentaire(
                    id_commentaire=row["id_commentaire"],
                    id_activite=row["id_activite"],
                    id_auteur=row["id_auteur"],
                    contenu=row["contenu"],
                    date_commentaire=row["date_commentaire"],
                )

                liste_commentaires.append(commentaire)

        return liste_commentaires


    @log
    def supprimer(self, id_commentaire: int) -> bool:
        """Suppression d'un commentaire dans la base de données

        Parameters
        ----------
        id_commentaire : int
            l'id du commentaire à supprimer de la base de données

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
                        {"id_commentaire": id_commentaire},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.error(e)
            raise

        return res > 0

    def trouver_par_id(self, id_commentaire: int) -> Commentaire:
        """Trouver un commentaire par son id"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM commentaire WHERE id_commentaire = %(id_commentaire)s;",
                        {"id_commentaire": id_commentaire}
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.error(e)
            raise

        commentaire = None
        if res:
            commentaire = Commentaire(
                id_commentaire=res["id_commentaire"],
                id_activite=res["id_activite"],
                id_auteur=res["id_auteur"],
                contenu=res["contenu"],
                date_commentaire=res["date_commentaire"]
            )
        return commentaire
        