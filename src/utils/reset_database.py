import os
import logging
import dotenv

from unittest import mock

from utils.log_decorator import log
from utils.singleton import Singleton
from dao.db_connection import DBConnection

from utils.securite import hash_password, generer_salt


class ResetDatabase(metaclass=Singleton):
    """
    Réinitialisation de la base de données
    """

    @log
    def lancer(self, test_dao=False):
        """Lancement de la réinitialisation des données
        Si test_dao = True : réinitialisation des données de test"""
        if test_dao:
            mock.patch.dict(os.environ, {"POSTGRES_SCHEMA": "projet_test_dao"}).start()
            pop_data_path = "data/pop_db_test.sql"
        else:
            pop_data_path = "data/pop_db.sql"

        dotenv.load_dotenv()

        schema = os.environ["POSTGRES_SCHEMA"]

        create_schema = (
            f"DROP SCHEMA IF EXISTS {schema} CASCADE; CREATE SCHEMA {schema};"
        )

        init_db = open("data/init_db.sql", encoding="utf-8")
        init_db_as_string = init_db.read()
        init_db.close()

        pop_db = open(pop_data_path, encoding="utf-8")
        pop_db_as_string = pop_db.read()
        pop_db.close()

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(create_schema)
                    cursor.execute(init_db_as_string)
                    cursor.execute(pop_db_as_string)

                    # Récupérer tous les credentials et remplacer les mots de passe bruts
                    cursor.execute(
                        "SELECT id_utilisateur, mot_de_passe_hash FROM credentials;"
                    )
                    credentials = cursor.fetchall()

                    for cred in credentials:
                        # mot_de_passe_hash contient temporairement le mot de passe en clair (ex: "mdp1")
                        mot_de_passe_clair = cred["mot_de_passe_hash"]
                        sel = generer_salt()
                        mot_de_passe_hash = hash_password(mot_de_passe_clair, sel)

                        cursor.execute(
                            """
                            UPDATE credentials
                            SET mot_de_passe_hash = %(hash)s, sel = %(sel)s
                            WHERE id_utilisateur = %(id)s;
                            """,
                            {
                                "hash": mot_de_passe_hash,
                                "sel": sel,
                                "id": cred["id_utilisateur"],
                            },
                        )

            logging.info("Base de données réinitialisée avec succès")
            return True

        except Exception as e:
            logging.error(f"Erreur lors du reset de la base de données : {e}")
            raise


if __name__ == "__main__":
    ResetDatabase().lancer()
    ResetDatabase().lancer(True)
