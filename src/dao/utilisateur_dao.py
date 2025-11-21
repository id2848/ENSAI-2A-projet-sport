import logging
from utils.log_decorator import log
from utils.securite import hash_password, generer_salt, verifier_mot_de_passe
from dao.db_connection import DBConnection

from business_object.utilisateur import Utilisateur

class UtilisateurDao:
    """Classe contenant les méthodes pour accéder aux utilisateurs de la base de données"""

   
    @log
    def verifier_pseudo_existant(self, pseudo: str) -> bool:
        """Vérifier si un pseudo est déjà utilisé dans la base de données"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT 1 FROM utilisateur WHERE pseudo = %(pseudo)s;",
                        {"pseudo": pseudo},
                    )
                    res = cursor.fetchone()
                    return res is not None  # Si un résultat est trouvé, le pseudo existe déjà
        except Exception as e:
            logging.error(f"Erreur lors de la vérification du pseudo {pseudo}: {e}")
            return False


    @log
    def creer(self, utilisateur: Utilisateur, mot_de_passe: str) -> bool:
        """Création d'un utilisateur et de ses credentials associés"""
        try:
            # Vérification si le pseudo existe déjà
            if self.verifier_pseudo_existant(utilisateur.pseudo):
                logging.error(f"L'utilisateur avec le pseudo {utilisateur.pseudo} existe déjà.")
                return False

            # Générer un sel et le hash correspondant
            sel = generer_salt()
            mot_de_passe_hash = hash_password(mot_de_passe, sel)

            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Étape 1 : création de l'utilisateur (id auto-généré)
                    cursor.execute(
                        """
                        INSERT INTO utilisateur (pseudo, nom, prenom, date_de_naissance, sexe)
                        VALUES (%(pseudo)s, %(nom)s, %(prenom)s, %(date_de_naissance)s, %(sexe)s)
                        RETURNING id_utilisateur;
                        """,
                        {
                            "pseudo": utilisateur.pseudo,
                            "nom": utilisateur.nom,
                            "prenom": utilisateur.prenom,
                            "date_de_naissance": utilisateur.date_de_naissance,
                            "sexe": utilisateur.sexe,
                        },
                    )
                    res = cursor.fetchone()
                    if not res:
                        raise Exception("Échec de la création de l'utilisateur.")

                    # Récupération de l'id auto-généré
                    utilisateur.id_utilisateur = res["id_utilisateur"]

                    # Étape 2 : insérer les credentials
                    cursor.execute(
                        """
                        INSERT INTO credentials (id_utilisateur, mot_de_passe_hash, sel)
                        VALUES (%(id_utilisateur)s, %(mot_de_passe_hash)s, %(sel)s);
                        """,
                        {
                            "id_utilisateur": utilisateur.id_utilisateur,
                            "mot_de_passe_hash": mot_de_passe_hash,
                            "sel": sel,
                        },
                    )

            logging.info(f"Utilisateur {utilisateur.pseudo} créé avec succès (id={utilisateur.id_utilisateur}).")
            return True

        except Exception as e:
            logging.error(f"Erreur lors de la création de l'utilisateur {utilisateur.pseudo}: {e}")
            return False


    @log
    def trouver_par_pseudo(self, pseudo: str) -> Utilisateur | None:
        """Trouver un utilisateur grâce à son pseudo

        Parameters
        ----------
        pseudo : str
            pseudo de l'utilisateur que l'on souhaite trouver

        Returns
        -------
        utilisateur : Utilisateur
            renvoie l'utilisateur' que l'on cherche par pseudo
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM utilisateur WHERE pseudo = %(pseudo)s;", 
                        {"pseudo": pseudo}
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.error(f"Erreur lors de la recherche de l'utilisateur par pseudo {pseudo}: {e}")
            return None

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
        return None

    @log
    def trouver_par_id(self, id_utilisateur: int) -> Utilisateur | None:
        """Trouver un utilisateur par son ID"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM utilisateur WHERE id_utilisateur = %(id_utilisateur)s;", 
                        {"id_utilisateur": id_utilisateur}
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.error(f"Erreur lors de la recherche de l'utilisateur par ID {id_utilisateur}: {e}")
            return None

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
        return None

    @log
    def lister_tous(self) -> list[Utilisateur]:
        """Lister tous les utilisateurs

        Parameters
        ----------
        None

        Returns
        -------
        liste_utilisateurs : list[Utilisateur]
            Renvoie la liste de tous les utilisateurs dans la base de données
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM utilisateur;"
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des utilisateurs: {e}")
            raise

        liste_utilisateurs = []

        if res:
            for row in res:
                utilisateur = Utilisateur(
                    id_utilisateur=row["id_utilisateur"],
                    pseudo=row["pseudo"],
                    nom=row["nom"],
                    prenom=row["prenom"],
                    date_de_naissance=row["date_de_naissance"],
                    sexe=row["sexe"],
                )
                liste_utilisateurs.append(utilisateur)

        return liste_utilisateurs

    @log
    def modifier(self, utilisateur: int) -> bool:
        """Modification d'un utilisateur dans la base de données

        Parameters
        ----------
        utilisateur : Utilisateur

        Returns
        -------
        created : bool
            True si la modification est un succès
            False sinon
        """
        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE utilisateur SET "
                        "pseudo = %(pseudo)s, "
                        "nom = %(nom)s, "
                        "prenom = %(prenom)s, "
                        "date_de_naissance = %(date_de_naissance)s, "
                        "sexe = %(sexe)s "
                        "WHERE id_utilisateur = %(id_utilisateur)s;",
                        {
                            "pseudo": utilisateur.pseudo,
                            "nom": utilisateur.nom,
                            "prenom": utilisateur.prenom,
                            "date_de_naissance": utilisateur.date_de_naissance,
                            "sexe": utilisateur.sexe,
                            "id_utilisateur": utilisateur.id_utilisateur,
                        },
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.error(f"Erreur lors de la modification de l'utilisateur: {e}")

        return res == 1

    @log
    def supprimer(self, id_utilisateur: int) -> bool:
        """Suppression d'un utilisateur dans la base de données

        Parameters
        ----------
        id_utilisateur : int
            l'id de l'utilisateur à supprimer de la base de données

        Returns
        -------
        True si l'utilisateur a bien été supprimé
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM utilisateur WHERE id_utilisateur = %(id_utilisateur)s;",
                        {"id_utilisateur": id_utilisateur},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.error(f"Erreur lors de la suppression de l'utilisateur: {e}")
            raise

        return res > 0


    @log
    def se_connecter(self, pseudo: str, mot_de_passe: str) -> Utilisateur | None:
        """Authentification d'un utilisateur via pseudo et mot de passe"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Récupérer l'utilisateur et son mot de passe haché via jointure
                    cursor.execute(
                        """
                        SELECT u.id_utilisateur, u.pseudo, u.nom, u.prenom, u.date_de_naissance, u.sexe,
                            c.mot_de_passe_hash, c.sel
                        FROM utilisateur u
                        JOIN credentials c ON u.id_utilisateur = c.id_utilisateur
                        WHERE u.pseudo = %(pseudo)s;
                        """,
                        {"pseudo": pseudo},
                    )
                    res = cursor.fetchone()

            if not res:
                logging.warning(f"Aucun utilisateur trouvé avec le pseudo {pseudo}")
                return None

            # Vérification du mot de passe
            if not verifier_mot_de_passe(mot_de_passe, res["sel"], res["mot_de_passe_hash"]):
                logging.warning(f"Mot de passe incorrect pour {pseudo}")
                return None

            # Création de l’objet métier Utilisateur
            utilisateur = Utilisateur(
                id_utilisateur=res["id_utilisateur"],
                pseudo=res["pseudo"],
                nom=res["nom"],
                prenom=res["prenom"],
                date_de_naissance=res["date_de_naissance"],
                sexe=res["sexe"],
            )

            return utilisateur

        except Exception as e:
            logging.error(f"Erreur lors de la connexion avec pseudo {pseudo}: {e}")
            return None
