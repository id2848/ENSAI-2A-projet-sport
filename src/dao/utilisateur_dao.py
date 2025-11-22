from typing import List

import logging
from utils.log_decorator import log
from utils.securite import hash_password, generer_salt, verifier_mot_de_passe
from dao.db_connection import DBConnection

from business_object.utilisateur import Utilisateur

from exceptions import DatabaseCreationError, DatabaseDeletionError, DatabaseUpdateError, NotFoundError, InvalidPasswordError

class UtilisateurDao:
    """Classe contenant les méthodes pour accéder aux utilisateurs de la base de données"""

    @log
    def creer(self, utilisateur: Utilisateur, mot_de_passe: str) -> bool:
        """Création d'un utilisateur et de ses credentials associés dans la base de données

        Parameters
        ----------
        utilisateur : Utilisateur
            L'objet Utilisateur contenant les informations personnelles à insérer
        mot_de_passe : str
            Le mot de passe en clair qui sera hashé et stocké dans les credentials

        Returns
        -------
        bool
            True si l'utilisateur et ses credentials ont été créés avec succès
        """
        try:
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
                    if res is None:
                        raise DatabaseCreationError("Echec de la création de l'utilisateur.")

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
                # Si on arrive ici, commit du bloc, sinon, rollback automatique (donc l'utilisateur et les credentials sont forcément créés ensemble)

            logging.info(f"Utilisateur {utilisateur.pseudo} créé avec succès (id={utilisateur.id_utilisateur}).")
            return True

        except Exception as e:
            logging.error(f"Erreur lors de la création de l'utilisateur {utilisateur.pseudo}: {e}")
            raise

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
        """Trouver un utilisateur par son identifiant

        Parameters
        ----------
        id_utilisateur : int
            L'identifiant de l'utilisateur recherché

        Returns
        -------
        Utilisateur | None
            L'objet Utilisateur correspondant si trouvé, sinon None
        """
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
    def lister_tous(self) -> List[Utilisateur]:
        """Lister tous les utilisateurs

        Parameters
        ----------
        None

        Returns
        -------
        List[Utilisateur]
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
    def modifier(self, utilisateur: Utilisateur) -> bool:
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
            raise
        
        if res < 1:
            msg_err = "Echec de la modification de l'utilisateur : aucune ligne retournée par la base"
            logging.error(msg_err)
            raise DatabaseUpdateError(msg_err)

        return True

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

        if res < 1:
            msg_err = "Echec de la suppression de l'utilisateur : aucune ligne retournée par la base"
            logging.error(msg_err)
            raise DatabaseDeletionError(msg_err)

        return True

    @log
    def verifier_pseudo_existant(self, pseudo: str) -> bool:
        """Vérifier si un pseudo est déjà utilisé dans la base de données

        Parameters
        ----------
        pseudo : str
            Le pseudo dont on veut vérifier l’existence

        Returns
        -------
        bool
            True si le pseudo existe déjà, False sinon
        """
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
            raise
    
    @log
    def verifier_id_existant(self, id_utilisateur: int) -> bool:
        """Vérifier si un utilisateur existe via son identifiant

        Parameters
        ----------
        id_utilisateur : int
            Identifiant de l’utilisateur à vérifier

        Returns
        -------
        bool
            True si l’utilisateur existe, False sinon
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT 1 FROM utilisateur WHERE id_utilisateur = %(id_utilisateur)s;",
                        {"id_utilisateur": id_utilisateur},
                    )
                    res = cursor.fetchone()
                    return res is not None
        except Exception as e:
            logging.error(f"Erreur lors de la vérification de l'id {id_utilisateur}: {e}")
            raise

    @log
    def se_connecter(self, pseudo: str, mot_de_passe: str) -> Utilisateur | None:
        """Authentification d'un utilisateur via pseudo et mot de passe

        Parameters
        ----------
        pseudo : str
            Le pseudo de l’utilisateur tentant de se connecter
        mot_de_passe : str
            Le mot de passe fourni lors de la connexion

        Returns
        -------
        Utilisateur | None
            L’objet Utilisateur correspondant si l’authentification réussit.
            None n’est jamais retourné car une exception est levée en cas d’échec.
        """
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

            if res is None:
                msg_err = f"Aucun utilisateur trouvé avec le pseudo {pseudo}"
                logging.error(msg_err)
                raise NotFoundError(msg_err)

            # Vérification du mot de passe
            if not verifier_mot_de_passe(mot_de_passe, res["sel"], res["mot_de_passe_hash"]):
                msg_err = f"Mot de passe incorrect pour {pseudo}"
                logging.error(msg_err)
                raise InvalidPasswordError(msg_err)

            # Création de l'objet métier Utilisateur
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
            logging.error(e)
            raise
