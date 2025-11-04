import logging
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.utilisateur import Utilisateur
from business_object.activite import Activite

class ActiviteDAO:
    def creer(self, activite: Activite) -> bool:
        """Création d'une activité dans la base de données"""
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO activite(
                            id_activite, id_utilisateur, sport, date_activite, distance, duree
                        )
                        VALUES (
                            %(id_activite)s, %(id_utilisateur)s, %(sport)s,
                            %(date_activite)s, %(distance)s, %(duree)s
                        )
                        RETURNING id_activite;
                        """,
                        {
                            "id_activite": activite.id_activite,
                            "id_utilisateur": activite.id_utilisateur,
                            "sport": activite.sport,
                            "date_activite": activite.date_activite,
                            "distance": activite.distance,
                            "duree": activite.duree,
                        }
                    )
                    res = cursor.fetchone()
                    connection.commit()
                    return res is not None
        except Exception as e:
            logging.error(f"Erreur lors de la création d'une activité : {e}")
            return False

    def trouver_par_id(self, id_utilisateur) -> Utilisateur:
        """Trouver un utilisateur par son id"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM utilisateur WHERE id_utilisateur = %(id_utilisateur)s;",
                        {"id_utilisateur": id_utilisateur}
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            raise

        utilisateur = None
        if res:
            utilisateur = Utilisateur(
                pseudo=res["pseudo"],
                nom=res["nom"],
                prenom=res["prenom"],
                date_de_naissance=res["date_de_naissance"],
                sexe=res["sexe"],
                id_utilisateur=res["id_utilisateur"]
            )
        return utilisateur

    def lister_par_utilisateur(self, id_utilisateur) -> list[Activite]:
        """Lister toutes les activités d'un utilisateur donné
        Parameters
        ----------
        id_utilisateur : int
        numéro id de l'utilisateur
        Returns
        ---------
        liste_activites : list[Activite]
        Liste de toutes les activités associées à cet utilisateur
        """
        try:
                with DBConnection().connection as connection:
                        with connection.cursor() as cursor:
                                cursor.execute(
                                        "SELECT * FROM activite WHERE id_utilisateur = %(id_utilisateur)s;",
                                        {"id_utilisateur": id_utilisateur}
                                )
                                res = cursor.fetchall()
        except Exception as e:
                logging.info(e)
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
                                duree=row["duree"]
                        )
                        liste_activites.append(activite)
        return liste_activites


    def modifier(self, utilisateur) -> bool:
        """Modification d'un utilisateur dans la base de données"""
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE utilisateur
                        SET pseudo=%(pseudo)s,
                            mot_de_passe_hash=%(mot_de_passe_hash)s,
                            nom=%(nom)s,
                            prenom=%(prenom)s,
                            date_de_naissance=%(date_de_naissance)s,
                            sexe=%(sexe)s
                        WHERE id_utilisateur=%(id_utilisateur)s;
                        """,
                        {
                            "pseudo": utilisateur.pseudo,
                            "mot_de_passe_hash": utilisateur.mot_de_passe_hash,
                            "nom": utilisateur.nom,
                            "prenom": utilisateur.prenom,
                            "date_de_naissance": utilisateur.date_de_naissance,
                            "sexe": utilisateur.sexe,
                            "id_utilisateur": utilisateur.id_utilisateur,
                        }
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)
        return res == 1

    def supprimer(self, utilisateur) -> bool:
        """Suppression d'un utilisateur dans la base de données"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM utilisateur WHERE id_utilisateur=%(id_utilisateur)s",
                        {"id_utilisateur": utilisateur.id_utilisateur}
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)
            raise
        return res > 0

    def se_connecter(self, pseudo, mot_de_passe_hash) -> Utilisateur:
        """Se connecter grâce à son pseudo et son mot de passe"""
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT *
                        FROM utilisateur
                        WHERE pseudo = %(pseudo)s
                        AND mot_de_passe_hash = %(mot_de_passe_hash)s;
                        """,
                        {"pseudo": pseudo, "mot_de_passe_hash": mot_de_passe_hash}
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        utilisateur = None
        if res:
            utilisateur = Utilisateur(
                pseudo=res["pseudo"],
                mot_de_passe_hash=res["mot_de_passe_hash"],
                nom=res["nom"],
                prenom=res["prenom"],
                date_de_naissance=res["date_de_naissance"],
                sexe=res["sexe"],
                id_utilisateur=res["id_utilisateur"]
            )
        return utilisateur
