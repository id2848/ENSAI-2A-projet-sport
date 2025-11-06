import logging
from utils.log_decorator import log
from utils.securite import hash_password
from dao.db_connection import DBConnection

from business_object.utilisateur import Utilisateur
import bcrypt
import hashlib
import os

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


    # Méthode dans `UtilisateurDao` pour créer un utilisateur

  
    @log
    def creer(self, utilisateur: Utilisateur) -> bool:
        """Création d'un utilisateur dans la base de données"""
        res = None

        # Vérification si l'utilisateur existe déjà
        if self.verifier_pseudo_existant(utilisateur.pseudo):
            logging.error(f"L'utilisateur avec le pseudo {utilisateur.pseudo} existe déjà.")
            return False  # L'utilisateur existe déjà

        try:
            # Génération d'un salt unique pour cet utilisateur (chaîne aléatoire)
            salt = os.urandom(16).hex()  # Génère un salt aléatoire de 16 octets (converti en hexadécimal)

            # Hachage du mot de passe avec SHA-256 et le salt
            mot_de_passe_hash = hash_password(utilisateur.mot_de_passe_hash, salt)

            # Insertion dans la base de données
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO utilisateur (pseudo, mot_de_passe_hash, nom, prenom, date_de_naissance, sexe, salt) "
                        "VALUES (%(pseudo)s, %(mot_de_passe_hash)s, %(nom)s, %(prenom)s, %(date_de_naissance)s, %(sexe)s, %(salt)s) "
                        "RETURNING id_utilisateur;",
                        {
                            "pseudo": utilisateur.pseudo,
                            "mot_de_passe_hash": mot_de_passe_hash,  # Haché avec SHA-256 et salt
                            "nom": utilisateur.nom,
                            "prenom": utilisateur.prenom,
                            "date_de_naissance": utilisateur.date_de_naissance,
                            "sexe": utilisateur.sexe,
                            "salt": salt  # Sauvegarde du salt dans la base de données
                        }
                    )
                    res = cursor.fetchone()  # Récupère l'ID de l'utilisateur créé
        except Exception as e:
            logging.error(f"Erreur lors de la création de l'utilisateur: {e}")
            return False  # Retourne False si l'insertion échoue

        if res:
            utilisateur.id_utilisateur = res["id_utilisateur"]
            return True
        return False

    @log
    def trouver_par_pseudo(self, pseudo) -> Utilisateur:
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
                id_utilisateur=res["id_utilisateur"],
                mot_de_passe_hash=res["mot_de_passe_hash"]
            )
            return utilisateur
        return None

    @log
    def trouver_par_id(self, id_utilisateur) -> Utilisateur:
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
                id_utilisateur=res["id_utilisateur"],
                mot_de_passe_hash=res["mot_de_passe_hash"]
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
                    mot_de_passe_hash=row["mot_de_passe_hash"],
                    nom=row["nom"],
                    prenom=row["prenom"],
                    date_de_naissance=row["date_de_naissance"],
                    sexe=row["sexe"],
                )
                liste_utilisateurs.append(utilisateur)

        return liste_utilisateurs

    @log
    def modifier(self, utilisateur) -> bool:
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
                        "mot_de_passe_hash = %(mot_de_passe_hash)s, "
                        "nom = %(nom)s, "
                        "prenom = %(prenom)s, "
                        "date_de_naissance = %(date_de_naissance)s, "
                        "sexe = %(sexe)s "
                        "WHERE id_utilisateur = %(id_utilisateur)s;",
                        {
                            "pseudo": utilisateur.pseudo,
                            "mot_de_passe_hash": utilisateur.mot_de_passe_hash,
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
    def supprimer(self, utilisateur) -> bool:
        """Suppression d'un utilisateur dans la base de données

        Parameters
        ----------
        utilisateur : Utilisateur
            Utilisateur à supprimer de la base de données

        Returns
        -------
        True si l'utilisateur a bien été supprimé
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM utilisateur WHERE id_utilisateur = %(id_utilisateur)s;",
                        {"id_utilisateur": utilisateur.id_utilisateur},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.error(f"Erreur lors de la suppression de l'utilisateur: {e}")
            raise

        return res > 0





    @log
    def se_connecter(self, pseudo: str, mot_de_passe: str) -> Utilisateur:
        """Se connecter grâce à son pseudo et son mot de passe"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM utilisateur WHERE pseudo = %(pseudo)s;", 
                        {"pseudo": pseudo}
                    )
                    res = cursor.fetchone()

            if res:
                # Récupérer le salt de l'utilisateur stocké en base de données
                salt = res["salt"]
                # Hachage du mot de passe fourni avec le même salt
                mot_de_passe_hash = hash_password(mot_de_passe, salt)
                
                # Comparer le mot de passe haché avec celui stocké en base de données
                if mot_de_passe_hash == res["mot_de_passe_hash"]:
                    utilisateur = Utilisateur(
                        pseudo=res["pseudo"],
                        mot_de_passe_hash=res["mot_de_passe_hash"],
                        nom=res["nom"],
                        prenom=res["prenom"],
                        date_de_naissance=res["date_de_naissance"],
                        sexe=res["sexe"],
                        id_utilisateur=res["id_utilisateur"],
                    )
                    return utilisateur  # Connexion réussie
                else:
                    logging.error(f"Mot de passe incorrect pour {pseudo}")
                    return None  # Mot de passe incorrect
            else:
                logging.error(f"Aucun utilisateur trouvé avec le pseudo {pseudo}")
                return None  # Utilisateur non trouvé
        except Exception as e:
            logging.error(f"Erreur lors de la connexion avec pseudo {pseudo}: {e}")
            return None
