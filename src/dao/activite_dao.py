import logging
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.utilisateur import Utilisateur
from business_object.activite import Activite

class ActiviteDao:
    def creer(self, activite: Activite) -> bool:
        """Création d'une activité dans la base de données"""
        res = None
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
                        }
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.error(f"Erreur lors de la création d'une activité : {e}")
            return False
        
        created = False
        if res:
            activite.id_activite = res["id_activite"]
            created = True

        return created

    def trouver_par_id(self, id_activite) -> Activite:
        """Trouver une activité par son id"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM activite WHERE id_activite = %(id_activite)s;",
                        {"id_activite": id_activite}
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
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


    def modifier(self, activite: Activite) -> bool:
        """Modifier une activité existante dans la base de données"""
        res = None
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
                            "duree": activite.duree
                        }
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)
        return res == 1

    
    def supprimer(self, activite: Activite) -> bool:
        """Supprimer une activité de la base de données"""
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM activite WHERE id_activite=%(id_activite)s;",
                        {"id_activite": activite.id_activite}
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)
            raise
        return res > 0

    def lister_par_utilisateur(self, id_utilisateur) -> list[Activite]:
        """Lister toutes les activités d'un utilisateur"""
        res = None
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
    
    def lister_activites_filtres(self, id_utilisateur, sport=None, date_debut=None, date_fin=None) -> list[Activite]:
        """Lister les activités d'un utilisateur avec des filtres optionnels (sport, date de début, date de fin)."""
        
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